'use strict';

var app = angular.module('ReleaseUI', ['ReleaseUI.controllers', 'ngRoute', 'ngResource', 'ngMaterial']);


app.config(function($routeProvider, $locationProvider) {
  $routeProvider
    .when('/dashboard', {
      templateUrl: 'app/partials/main.html',
      controller: 'MainController'
    })
    .when('/login', {
      templateUrl: 'app/partials/login.html',
      controller: 'LoginController'
    })
    .when('/:release_id', {
      templateUrl: 'app/partials/details.html',
      controller: 'DetailsController'
    })
    .otherwise({
      redirectTo: '/login'
    });
}).run(function($rootScope, $location) {
  $rootScope.$on("$routeChangeStart", function(event, next, current) {
    console.log(localStorage.getItem('loggedIn'));
    if (localStorage.getItem('loggedIn') == null) {
      // no logged user, redirect to /login
      if ( next.templateUrl === "app/partials/login.html") {
      } else {
        $location.path("/login");
      }
    }
  });
});
