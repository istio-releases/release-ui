'use strict';

/* Controllers */

var app = angular.module('ReleaseUI.controllers', ['ngStorage', 'firebase']);

app.controller('MainController', ['$scope','$http','$location','$log', '$sessionStorage',
  function($scope, $http, $location, $log, $sessionStorage) {

    // Set static variables
    $scope.numPerPage = 15;
    $scope.numRequested = 45;
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

    $scope.stateValues = [
      {"id":2, "status": "Finished"},
      {"id":3, "status": "Failed"},
      {"id":1, "status": "Pending"},
      {"id":4, "status": "Suspended"},
    ];

    // Set default values for storage
    var defaultStorage = {
      stateValue: null,
      currentPage: 1,
      maxDate: new Date(),
      maxFromDate: new Date(),
      minToDate: new Date(0),
      fromDate: new Date(0),
      toDate: new Date(),
      startDate: null,
      endDate: null,
      whichDate: 'started',
      labelValue: null,
      sortMethod: 3,
      releases: []
    };
    $scope.$storage = $sessionStorage.$default(defaultStorage);

    // Instantiates variables in scope based on stored information
    var setScope = function () {
      $scope.maxDate = new Date($scope.$storage.maxDate);
      $scope.maxFromDate = new Date($scope.$storage.maxFromDate);
      $scope.minToDate = new Date($scope.$storage.minToDate);
      $scope.fromDate = new Date($scope.$storage.fromDate);
      $scope.toDate = new Date($scope.$storage.toDate);
      $scope.filterDate = $scope.$storage.whichDate;

      if ($scope.$storage.startDate != null ) {
        $scope.startDate = new Date($scope.$storage.startDate);
      }
      if ($scope.$storage.endDate != null){
        $scope.endDate = new Date($scope.$storage.endDate);
      }

      $scope.selectedValue = $scope.$storage.stateValue;
      $scope.selectedLabel = $scope.$storage.labelValue;
    };

    // Set Scope when loading page
    setScope();

    // HTTP Request to get release information
    var getReleases = function (method) {

      var state;
      if($scope.$storage.stateValue == null) {
        state = 0;
      }
      else {
        state = $scope.$storage.stateValue;
      }

      var start = new Date($scope.$storage.fromDate);
      start = Math.floor(start.getTime() / 1000);
      var end = new Date($scope.$storage.toDate);
      end = Math.ceil(end.getTime() / 1000);

      var offset;
      if (method == 'page') {
        offset = $scope.$storage.releases.length;
      }
      else if (method == 'onload') {
        offset = 0;
      }
      else {
        offset = 0;
        $scope.$storage.currentPage = 1;
      }

      var url_string = 'http://localhost:8080/releases?state=' + state +
          '&label=' + $scope.$storage.labelValue + '&start_date=' + start +
          '&end_date=' + end + '&datetype=' + $scope.$storage.whichDate +
          '&sort_method='+ $scope.$storage.sortMethod + '&limit=' + $scope.numRequested +
          '&offset=' + offset;

      $http({
           method: 'GET',
           url: url_string,
           cache: true
       }).then(function successCallback(response) {
          var data = transform(response.data);
          if (method == 'page') {
            $scope.$storage.releases = $scope.$storage.releases.concat(data);
          }
          else {
            $scope.$storage.releases = data;
          }
           $scope.totalPages = Math.ceil($scope.$storage.releases.length / $scope.numPerPage);
           $log.log('request successful');
       }, function errorCallback(response) {
           $log.log(response);
       });
    };
    getReleases('onload');

    // onclick/onchange functions that may request more data from server
    $scope.dateChange = function (from, input) {
      if (from) {
        $scope.$storage.fromDate = input;
        $scope.$storage.minToDate = input;
        $scope.$storage.startDate = input;
      }
      else {
        $scope.$storage.toDate = input;
        $scope.$storage.maxFromDate = input;
        $scope.$storage.endDate = input;
      }
      setScope();
      getReleases('onDateChange');
    };

    $scope.dateTypeChange = function (input) {
      if (input == 0) {
        $scope.$storage.whichDate = 'started';
        $scope.$storage.sortMethod = 3;
      }
      else {
        $scope.$storage.whichDate = 'last_modified';
        $scope.$storage.sortMethod = 5;
      }
      setScope();
      getReleases('onDateTypeChange');
    };

    $scope.filterChange = function (status, input) {
      if (status) {
        $scope.$storage.stateValue = input;
        $scope.$storage.selectedValue = input;
      }
      else {
        $scope.$storage.labelValue = input;
        $scope.$storage.selectedLabel = input;
      }
      setScope();
      getReleases('onFilterChange');
    };

    $scope.sortChange = function (input) {
      if ($scope.$storage.sortMethod % 2 == 0) {
        $scope.$storage.sortMethod = input;
      }
      else {
        $scope.$storage.sortMethod = input + 1;
      }
      getReleases('onSortChange');
    };

    $scope.pageChange = function (input) {
      if (input == -2) {
        $scope.$storage.currentPage = 1;
      }
      else if ($scope.$storage.currentPage + input < $scope.totalPages - 1){
        $scope.$storage.currentPage = $scope.$storage.currentPage + input;
      }
      else {
        getReleases('page');
        $scope.$storage.currentPage = $scope.$storage.currentPage + input;
      }
    };

    // Reset Filters and OrderBy
    $scope.resetFilter = function () {	{



	}
      // Reset default settings and scope
      $sessionStorage.$reset(defaultStorage);
      setScope();

      // Reset dropdowns in UI
      $scope.defaultStatus = true;
      $scope.defaultLabel = true;
      $scope.startDate = null;
      $scope.endDate = null;

      getReleases('onload');
    };

    // Redirect to Details function onclick of table row
    $scope.redirectToDetails = function (input) {
      var newRoute = '/' + input.name;
      $location.path(newRoute);
    };
}]);

app.controller('DetailsController', ['$scope', '$location', '$log', '$http', '$routeParams',
  function ($scope, $location, $log, $http, $routeParams) {

    var release_name = $routeParams.releasename;

    // Request release details
    $http({
         method: 'GET',
         url: 'http://localhost:8080/release?release=' + release_name,
         cache: true
     }).then(function successCallback(response) {
         $scope.release = angular.fromJson(response.data);
     }, function errorCallback(response) {
         $log.log(response);
     });

    // Request task details
    $http({
         method: 'GET',
         url: 'http://localhost:8080/tasks?release=' + release_name,
         cache: true
     }).then(function successCallback(response) {
          $scope.tasks = transform(response.data);
     }, function errorCallback(response) {
         $log.log(response);
     });
}]);

// Transforms json data to array
function transform(input) {
  input = angular.fromJson(input);
  var output = [], item;

  angular.forEach(input, function(item) {
    output.push(item);
  });
   return output;
}
