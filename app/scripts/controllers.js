'use strict';

/* Controllers */

var app = angular.module('ReleaseUI.controllers', []);

app.controller('MainController', ['$scope','$http','$location','$log','serviceRelease',
  function($scope, $http, $location, $log, serviceRelease) {

    // Get information from http request
    var labelSet = new Set();
    var labels;
    $http({
      method: 'GET',
      url: 'http://localhost:8080/releases',
      cache: true
    }).then(function successCallback(response) {
      var releases = angular.fromJson(response.data);
      angular.forEach(releases, function(value, key) {
        for (var i = 0; i < value.labels.length; i++) {
          labelSet.add(value.labels[i]);
        }
      });
      $scope.releases = releases;
      $scope.labels = Array.from(labelSet);
      labels = $scope.labels;
    }, function errorCallback(response) {
      $log.log(response);
    });

    // Starting settings for datepicker
    $scope.maxDate = new Date();
    $scope.maxFromDate = $scope.maxDate;
    $scope.minToDate = new Date(0);
    $scope.fromDate = $scope.minToDate;
    $scope.toDate = $scope.maxDate;
    $scope.whichDate = 'started';
    $scope.filterDate = 'started';

    // Starting settings for label filtered
    $scope.labelValue = null;

    // Starting settings for search filter
    $scope.searchTable = undefined;

    // Starting settings for state filter
    $scope.stateValues = [
      {"id":2, "status": "Finished"},
      {"id":3, "status": "Failed"},
      {"id":1, "status": "Pending"},
      {"id":4, "status": "Suspended"},
    ];
    $scope.stateValue = null;

    // Starting Settings for OrderBy filter
    $scope.sortType = 'last_modified';
    $scope.sortReverse = true;

    // Reset Filters and OrderBy
    $scope.resetFilter = function () {
      $scope.fromDate = new Date(0);
      $scope.toDate = new Date();
      $scope.startDate = null;
      $scope.endDate = null;
      $scope.whichDate = 'started';
      $scope.filterDate = 'started';

      $scope.labelValue = null;
      $scope.selectedLabel = null;

      $scope.stateValue = null;
      $scope.selectedValue = null;

      $scope.sortType = 'last_modified';
      $scope.sortReverse = true;
    };

    // Redirect to Details function
    $scope.redirectToDetails = function (input) {
      serviceRelease.set(input);
      $location.path('/details');
    }
}]);

app.controller('DetailsController', ['$scope','serviceRelease', function ($scope, serviceRelease) {
  $scope.release = serviceRelease.get();
}]);
