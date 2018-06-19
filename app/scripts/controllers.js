'use strict';

/* Controllers */

var app = angular.module('ReleaseUI.controllers', ['ngTable','ngStorage']);

app.controller('MainController', ['$scope','$http','$location','$log','serviceRelease', '$localStorage',
  function($scope, $http, $location, $log, serviceRelease, $localStorage) {

    // Starting settings for pagination
    $scope.currentPage = 1;
    $scope.numPerPage = 15;
    $scope.numRequested = 45;

    // Starting settings for datepicker
    $scope.maxDate = new Date();
    $scope.maxFromDate = $scope.maxDate;
    $scope.minToDate = new Date(0);
    $scope.fromDate = $scope.minToDate;
    $scope.toDate = $scope.maxDate;
    $scope.filterDate = 'started';
    $scope.whichDate = 'started';

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
      });
    };
    getLabels();
    $scope.labelValue = null;

    // Starting settings for state filter
    $scope.stateValues = [
      {"id":2, "status": "Finished"},
      {"id":3, "status": "Failed"},
      {"id":1, "status": "Pending"},
      {"id":4, "status": "Suspended"},
    ];

    // Starting settings for sort
    $scope.sortMethod = 3;

    // Redirect to Details function onclick of table row
    $scope.redirectToDetails = function (input) {
      serviceRelease.set(input, $scope.releases);
      var newRoute = '/' + input.name;
      $location.path(newRoute);
    };

    // Helper function that makes gets releases
    var getReleases = function (isPage) {

      var state;
      if($scope.stateValue == null) {
        state = 0;
      }
      else {
        state = $scope.stateValue;
      }

      var start = Math.floor($scope.fromDate.getTime() / 1000);
      var end = Math.ceil($scope.toDate.getTime() / 1000);

      var offset;
      if (isPage) {
        offset = $scope.releases.length;
      }
      else {
        offset = 0;
        $scope.currentPage = 1;
      }

      var url_string = 'http://localhost:8080/page?state=' + state +
          '&label=' + $scope.labelValue + '&start_date=' + start +
          '&end_date=' + end + '&datetype=' + $scope.whichDate +
          '&sort_method='+ $scope.sortMethod + '&limit=' + $scope.numRequested +
          '&offset=' + offset;

      $http({
           method: 'POST',
           url: url_string,
           cache: true
       }).then(function successCallback(response) {
          if (isPage) {
            $scope.releases = $scope.releases.concat(toArray(angular.fromJson(response.data)));
          }
          else {
            $scope.releases = toArray(angular.fromJson(response.data));
          }
           $scope.totalPages = Math.ceil($scope.releases.length / $scope.numPerPage);
           $log.log('request successful');
       }, function errorCallback(response) {
           $log.log(response);
       });
    };
    getReleases(false);

    // onclick/onchange functions that may request more data from server
    $scope.dateChange = function (from, input) {
      if (from) {
        $scope.fromDate = input;
        $scope.minToDate = input;
      }
      else {
        $scope.toDate = input;
        $scope.maxFromDate = input;
      }
      getReleases(false);
    };

    $scope.filterChange = function (status, input) {
      if (status) {
        $scope.stateValue = input;
      }
      else {
        $scope.labelValue = input;
      }
      getReleases(false);
    };

    $scope.sortChange = function (input) {
      if ($scope.sortMethod % 2 == 0) {
        $scope.sortMethod = input;
      }
      else {
        $scope.sortMethod = input + 1;
      }
      getReleases(false);
    };

    $scope.pageChange = function (input) {
      if (input == -2) {
        $scope.currentPage = 1;
      }
      else if ($scope.currentPage + input < $scope.totalPages - 1){
        $scope.currentPage = $scope.currentPage + input;
      }
      else {
        getReleases(true);
        $scope.currentPage = $scope.currentPage + input;
      }
    };

    // Reset Filters and OrderBy
    $scope.resetFilter = function () {
      $scope.maxDate = new Date();
      $scope.maxFromDate = $scope.maxDate;
      $scope.minToDate = new Date(0);
      $scope.fromDate = $scope.minToDate;
      $scope.toDate = $scope.maxDate;
      $scope.startDate = null;
      $scope.endDate = null;
      $scope.filterDate = 'started';
      $scope.whichDate = 'started';

      $scope.labelValue = null;
      $scope.selectedLabel = "";

      $scope.stateValue = null;
      delete $scope.selectedValue;

      $scope.sortType = 3;
      getReleases(false);
      $log.log()
    };
}]);

app.controller('DetailsController', ['$scope','serviceRelease', '$location', '$log', '$http',
function ($scope, serviceRelease, $location, $log, $http) {
  $scope.release = serviceRelease.get();

  // Request specific task details
  $http({
       method: 'POST',
       url: 'http://localhost:8080/tasks?release=' + $scope.release.name,
       cache: true
   }).then(function successCallback(response) {
        $scope.tasks = toArray(angular.fromJson(response.data));
   }, function errorCallback(response) {
       $log.log(response);
   });

  // Return to main dashboard
  $scope.homePage = function() {
    $location.path('/');
  };

}]);

// Helper function that turns object to array
function toArray(input) {
  var output = [], item;

  angular.forEach(input, function(item) {
    output.push(item);
  });
   return output;
}
