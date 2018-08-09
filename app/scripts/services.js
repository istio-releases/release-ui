'use strict';

/* Services */
var auth_org = 'istio-releases';
var auth_team = 'release-ui';
var app = angular.module('ReleaseUI.services', ['firebase']);

app.factory('Auth', ['$firebaseAuth',
  function($firebaseAuth) {
    return $firebaseAuth();
  }
]);

app.factory('Token',function(){
  var token;

  return {
    setToken: setToken,
    isAuth: isAuth
  };

  var setToken = function(t) {
    token = t;
  };
  
  var isAuth = function () {
    return $http({
          method: 'GET',
          url: 'https://api.github.com/user/teams',
          headers: {'Authorization': 'token ' + token}
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
})

app.service('ReleaseData', function() {
  var release = {};

  var setRelease = function(value) {
      release = value;
  };

  var getRelease = function() {
      return release;
  };

  return {
    setRelease: setRelease,
    getRelease: getRelease
  };
});
