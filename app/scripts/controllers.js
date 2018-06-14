'use strict';

/* Controllers */

var app = angular.module('ReleaseUI.controllers', ['ngTable']);

app.controller('MainController', ['$scope','$http','$location','$log','serviceRelease', 'NgTableParams',
  function($scope, $http, $location, $log, serviceRelease, NgTableParams) {

    $scope.releases = [];

    // pagination
    $scope.currentPage = 1;
    $scope.numPerPage = 10;
    $scope.totalPages = 0;
    $scope.totalReleases = 30;

    // Starting settings for datepicker
    $scope.maxDate = new Date();
    $scope.maxFromDate = $scope.maxDate;
    $scope.minToDate = new Date(0);
    $scope.fromDate = $scope.minToDate;
    $scope.toDate = $scope.maxDate;
    $scope.whichDate = 'started';
    $scope.filterDate = 'started';

    // Starting settings for Labels
    var getLabels = function () {
      $http({
                method: 'GET',
                url: 'http://localhost:8080/labels',
                cache: true
            }).then(function successCallback(response) {
                $scope.labels = angular.fromJson(response.data);
            }, function errorCallback(response) {
                $log.log(response);
            })
    };
    getLabels();
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

    // Redirect to Details function
    $scope.redirectToDetails = function (input) {
      serviceRelease.set(input);
      $location.path('/details');
    };

    // Helper function for post http requests
    var helper = function () {
      var method = $scope.sortType;
      var reverse = $scope.sortReverse;
      var sort_method;

      if(method == 'name' && reverse) {
        sort_method = 1;
      }
      else if (method == 'name') {
        sort_method = 2;
      }
      else if (method == 'started' && reverse) {
        sort_method = 3;
      }
      else if (method == 'started') {
        sort_method = 4;
      }
      else if(method == 'last_modified' && reverse) {
        sort_method = 5;
      }
      else if (method == 'last_modified') {
        sort_method = 6;
      }
      else if (method == 'last_active_task' && reverse) {
        sort_method = 7;
      }
      else if (method == 'last_active_task') {
        sort_method = 8;
      }

      var state;
      if($scope.stateValue == null) {
        state = 0;
      }
      else {
        state = $scope.stateValue;
      }

      var datetype;
      if ($scope.whichDate == 'started') {
        datetype = 0;
      }
      else {
        datetype = 1;
      }

      var start = Math.floor($scope.fromDate.getTime() / 1000);
      var end = Math.ceil($scope.toDate.getTime() / 1000);

      var url_string = 'http://localhost:8080/page?state=' + state +
                   '&label=' + $scope.labelValue + '&start_date=' + start +
                   '&end_date=' + end + '&datetype=' + datetype +
                   '&sort_method='+ sort_method + '&limit=' + $scope.totalReleases + '&offset=' + $scope.releases.length;
      $log.log(url_string);
      $http({
          method: 'POST',
          url: url_string,
          cache: true
      }).then(function successCallback(response) {
          $scope.releases = $scope.releases.concat(toArray(angular.fromJson(response.data)));
          $scope.lastDate = $scope.releases[$scope.releases.length - 1].last_modified;
          $scope.totalPages = Math.ceil($scope.releases.length / $scope.numPerPage);
          $log.log('request made');
      }, function errorCallback(response) {
          $log.log(response);
      });

    };
    helper();

    // functions that may request more data from server
    $scope.fromDateChange = function (input) {
      $scope.fromDate = input;
      $scope.minToDate = input;
      $scope.currentPage = 1;
    };

    $scope.toDateChange = function (input) {
      $scope.toDate = input;
      $scope.maxFromDate = input;
      $scope.currentPage = 1;
    };

    $scope.statusFilterChange = function (input) {
      $log.log($scope.filteredReleases);
      $scope.stateValue = input;
      $scope.currentPage = 1;

    };

    $scope.sortChange = function (input) {
      $scope.sortType = input;
      $scope.sortReverse = !$scope.sortReverse;
      $scope.currentPage = 1;

    };

    $scope.labelFilterChange = function (input) {
      $scope.labelValue = input;
      $scope.currentPage = 1;

    };

    $scope.pageChange = function (input) {
      if (input == -2) {
        $scope.currentPage = 1;
      }
      else {
        $scope.currentPage = $scope.currentPage + input;
      }
      if($scope.currentPage >= $scope.totalPages - 1) {
        helper();
      }
    };

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
      helper();
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
