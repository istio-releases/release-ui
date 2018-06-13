'use strict';

/* Controllers */

var app = angular.module('ReleaseUI.controllers', ['ngTable']);

app.controller('MainController', ['$scope','$http','$location','$log','serviceRelease', 'NgTableParams',
  function($scope, $http, $location, $log, serviceRelease, NgTableParams) {

    // Get information from http request
    var labelSet = new Set();

    // pagination
    $scope.currentPage = 1;
    $scope.numPerPage = 9;
    $scope.filteredReleases = [];

    $scope.getReleases = function () {
      return $http({
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
        $scope.labels = Array.from(labelSet);
        $scope.releases = releases;
        $scope.totalPages = Math.ceil(Object.keys($scope.releases).length / $scope.numPerPage);
      }, function errorCallback(response) {
        $log.log(response);
      });
    };
    $scope.getReleases();

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
    };

    // functions that may request more data from server
    $scope.fromDateChange = function (input) {
      $scope.fromDate = input;
      $scope.minToDate = input;
      // request more data from backend
    };

    $scope.toDateChange = function (input) {
      $scope.toDate = input;
      $scope.maxFromDate = input;
      // request more data from backend
    };

    $scope.statusFilterChange = function (input) {
      $scope.stateValue = input;
      $log.log($scope.filteredReleases);
      $log.
      $scope.totalPages = Math.floor(Object.keys($scope.filteredReleases).length / $scope.numPerPage);
      // request more data from backend
    };

    $scope.sortChange = function (input) {
      $scope.sortType = input;
      $scope.sortReverse = !$scope.sortReverse;
      //request more data from backend
    };

    $scope.labelFilterChange = function (input) {
      $scope.labelValue = input;
      //request more data
    }


    $scope.pageChange = function (input) {
      $scope.currentPage = $scope.currentPage + input;
      if($scope.currentPage == $scope.totalPages) {
        // request more data from backend
      }
    };

}]);

app.controller('DetailsController', ['$scope','serviceRelease', function ($scope, serviceRelease) {
  $scope.release = serviceRelease.get();
}]);

function toArray(input) {
  var output = [], item;

  angular.forEach(input, function(item) {
    output.push(item);
  });
   return output;
}
