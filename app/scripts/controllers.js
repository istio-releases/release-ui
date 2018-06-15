'use strict';

/* Controllers */

var app = angular.module('ReleaseUI.controllers', ['ngTable']);

app.controller('MainController', ['$scope','$http','$location','$log','serviceRelease', 'NgTableParams', '$filter',
  function($scope, $http, $location, $log, serviceRelease, NgTableParams, $filter) {

    $scope.releases = [];

    // pagination
    $scope.currentPage = 1;
    $scope.numPerPage = 10;
    $scope.totalPages = 0;
    $scope.totalReleases = 30;
    $scope.numRequested = 30;

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

    // Helper function that makes URL for post request
    var requestURL = function () {
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

      var offset;
      var limit;
      if ($scope.currentPage == -1) {
        offset = -30;
        limit = $scope.numRequested
      }
      else {
        offset = $scope.releases.length;
        limit = $scope.numRequested
      }

      return 'http://localhost:8080/page?state=' + state +
                   '&label=' + $scope.labelValue + '&start_date=' + start +
                   '&end_date=' + end + '&datetype=' + datetype +
                   '&sort_method='+ sort_method + '&limit=' + $scope.numRequested + '&offset=' + $scope.releases.length;
    };

    // First HTTP request when page opens
    $http({
        method: 'POST',
        url: requestURL(),
        cache: true
    }).then(function successCallback(response) {
        $scope.releases = toArray(angular.fromJson(response.data));
        $scope.lastDate = $scope.releases[$scope.releases.length - 1].last_modified;
        $scope.totalPages = Math.ceil($scope.releases.length / $scope.numPerPage);
        $log.log('request made');
    }, function errorCallback(response) {
        $log.log(response);
    });

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
      $scope.stateValue = input;
      $scope.currentPage = 1;
      $scope.filteredReleases = $filter('propFilter')($scope.releases, $scope.stateValue, $scope.labelValue, $scope.fromDate, $scope.toDate, $scope.whichDate);
      if ($scope.filteredReleases.length <= $scope.totalReleases) {
        $scope.releases = [];
        $scope.numRequested = $scope.totalReleases - $scope.filteredReleases.length;
        $http({
            method: 'POST',
            url: requestURL(),
            cache: true
        }).then(function successCallback(response) {
            $scope.releases = toArray(angular.fromJson(response.data));
            $scope.filteredReleases = $filter('propFilter')($scope.releases, $scope.stateValue, $scope.labelValue, $scope.fromDate, $scope.toDate, $scope.whichDate);
            $scope.totalPages = Math.ceil($scope.filteredReleases.length / $scope.numPerPage);
            $log.log('request made');
        }, function errorCallback(response) {
            $log.log(response);
        });
      }
    };

    $scope.sortChange = function (input) {
      $scope.sortType = input;
      $scope.sortReverse = !$scope.sortReverse;
      $scope.currentPage = 1;

    };

    $scope.labelFilterChange = function (input) {
      $scope.labelValue = input;
      $scope.currentPage = 1;
      $scope.filteredReleases = $filter('propFilter')($scope.releases, $scope.stateValue, $scope.labelValue, $scope.fromDate, $scope.toDate, $scope.whichDate);
      if ($scope.filteredReleases.length <= $scope.totalReleases) {
        $scope.releases = [];
        $scope.numRequested = $scope.totalReleases - $scope.filteredReleases.length;
        $http({
            method: 'POST',
            url: requestURL(),
            cache: true
        }).then(function successCallback(response) {
            $scope.releases = toArray(angular.fromJson(response.data));
            $scope.filteredReleases = $filter('propFilter')($scope.releases, $scope.stateValue, $scope.labelValue, $scope.fromDate, $scope.toDate, $scope.whichDate);
            $log.log('request made');
        }, function errorCallback(response) {
            $log.log(response);
        });
      }
      $scope.totalPages = Math.ceil($scope.filteredReleases.length / $scope.numPerPage);

    };

    $scope.pageChange = function (input) {
      if (input == -2) {
        $scope.currentPage = 1;
      }
      else if ($scope.currentPage + input < $scope.totalPages - 1){
        $scope.currentPage = $scope.currentPage + input;
      }
      else {
        $http({
            method: 'POST',
            url: requestURL(),
            cache: true
        }).then(function successCallback(response) {
            $scope.releases = $scope.releases.concat(toArray(angular.fromJson(response.data)));
            $scope.filteredReleases = $filter('propFilter')($scope.releases, $scope.stateValue, $scope.labelValue, $scope.fromDate, $scope.toDate, $scope.whichDate);
            $scope.totalPages = Math.ceil($scope.filteredReleases.length / $scope.numPerPage);
            $log.log('request made');
        }, function errorCallback(response) {
            $log.log(response);
        });
        $scope.currentPage = $scope.currentPage + input;
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
      requestData();
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
