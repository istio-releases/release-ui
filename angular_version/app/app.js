'use strict';

var App = angular.module('ReleaseUI', ['ngRoute', 'ngResource', 'ngMaterial', 'releaseUI.main', 'releaseUI.details']);

App.config(function($routeProvider) {
  $routeProvider
    .otherwise({redirectTo: '/'});
});
