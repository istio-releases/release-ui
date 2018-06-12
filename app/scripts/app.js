'use strict';
var App = angular.module('ReleaseUI', ['ReleaseUI.controllers', 'ReleaseUI.filters','ngRoute', 'ngResource', 'ngMaterial', 'ReleaseUI.controllers']);

App.config(['$routeProvider', function($routeProvider) {
  $routeProvider
  .when('/', {
    templateUrl: 'app/partials/main.html',
    controller: 'MainController'
  })
  .when('/details', {
    templateUrl: 'app/partials/details.html',
    controller: 'DetailsController'
  })
  .otherwise({
    redirectTo: '/'
  });
}]);
