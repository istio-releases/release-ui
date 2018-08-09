'use strict';

/* Services */
var auth_org = 'wrong';
var auth_team = 'wrong';
var app = angular.module('ReleaseUI.services', ['firebase'])
                 .constant('auth_org', 'istio-releases')
                 .constant('auth_team', 'release-ui');

app.factory('Auth', ['$firebaseAuth',
  function($firebaseAuth) {
    return $firebaseAuth();
  }
]);

app.service('Token', ['$http', 'auth_org', 'auth_team',
  function($http, auth_org, auth_team) {

    var setToken = function(t) {
      localStorage.setItem('token', t);
    };

    var removeToken = function () {
      localStorage.removeItem('token');
    }

    var isAuth = function () {
      console.log(localStorage.getItem('token'));
      return $http({
            method: 'GET',
            url: 'https://api.github.com/user/teams',
            headers: {'Authorization': 'token ' + localStorage.getItem('token')}
          }).then(function successCallback(response) {
            var teams = response.data;
            for (var key in teams) {
             if (teams.hasOwnProperty(key)){
               var name = teams[key].name;
               var org = teams[key].organization.login;

               if (name == auth_team && org == auth_org){
                 console.log('Authenticated');
                 return true;
               }
             }
            }
            return false;
        }, function errorCallback(response) {
            console.log(response);
        });
    };

    return {
      setToken: setToken,
      removeToken: removeToken,
      isAuth: isAuth
    };
}]);
