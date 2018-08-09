'use strict';

var app = angular.module('ReleaseUI', ['ReleaseUI.controllers', 'ReleaseUI.services', 'ngRoute', 'ngResource', 'ngMaterial']);

app.run(['$rootScope', '$location', function($rootScope, $location) {
  $rootScope.$on('$routeChangeError', function(event, next, previous, error) {
    // We can catch the error thrown when the $requireSignIn promise is rejected
    // and redirect the user back to the home page
    if (error === 'AUTH_REQUIRED') {
      $location.path('/login');
    }
  });
}]);

app.config(['$routeProvider', function($routeProvider) {
  $routeProvider
    // Public Route
    .when('/login', {
      templateUrl: 'app/partials/login.html',
      controller: 'LoginController'
    })
    // Authenticated Routes
    .when('/create-release', {
      templateUrl: 'app/partials/create-release.html',
      controller: 'FormController',
      resolve: {
        'currentAuth': ['Auth', function(Auth) {
          return Auth.$requireSignIn();
        }]
      }
    })
    // Logged In Routes
    .when('/dashboard', {
      controller: 'MainController',
      templateUrl: 'app/partials/main.html',
      resolve: {
        'currentAuth': ['Auth', function(Auth) {
          return Auth.$requireSignIn();
        }]
      }
    })
    .when('/:release_id', {
      templateUrl: 'app/partials/details.html',
      controller: 'DetailsController',
      resolve: {
        'currentAuth': ['Auth', function(Auth) {
          return Auth.$requireSignIn();
        }]
      }
    })
    .when('/:release_id/:task_name/logs', {
      templateUrl: 'app/partials/logs.html',
      controller: 'LogsController',
      resolve: {
        'currentAuth': ['Auth', function(Auth) {
          return Auth.$requireSignIn();
        }]
      }
    })
    .otherwise({
      redirectTo: '/login'
    });
}]).run(function($rootScope, $location, Token) {
  // Extra Authentication requirements for create-release
  $rootScope.$on("$routeChangeStart", function(event, next, current) {
    if (next.templateUrl === "app/partials/create-release.html") {
      Token.isAuth().then((result) => {
        if (result) {
        }
        else {
          event.preventDefault();
          $location.path('/dashboard');
        }
      });
    }
  });
});
