'use strict';

angular.module('releaseUI.getReleases', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/getReleases', {
    templateUrl: '/getReleases',
    controller: 'getReleasesController'
  });
}])

.controller('getReleasesController', [function() {

}]);
