'use strict';

angular.module('releaseUI.details', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/details', {
    templateUrl: 'details/details.html',
    controller: 'DetailsController'
  });
}])

.controller('DetailsController', [function() {

}]);
