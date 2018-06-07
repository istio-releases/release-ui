'use strict';

var App = angular.module('ReleaseUI', ['ngRoute']);

App.config(function($routeProvider) {
$routeProvider
    .when('/', {
        templateUrl: '/partials/main.html',
        controller: 'MainController'
    });
});
