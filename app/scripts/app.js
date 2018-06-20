'use strict';
var App = angular.module('ReleaseUI', ['ReleaseUI.controllers', 'ReleaseUI.filters','ngRoute', 'ngResource', 'ngMaterial', 'ReleaseUI.services']);

App.config(['$routeProvider', function($routeProvider) {
  $routeProvider
  .when('/', {
    templateUrl: 'app/partials/main.html',
    controller: 'MainController'
  })
  .when('/:releasename', {
    templateUrl: 'app/partials/details.html',
    controller: 'DetailsController'
  })
  .otherwise({
    redirectTo: '/'
  });
}]);
