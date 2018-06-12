'use strict';
var releases;
var labels;

var app = angular.module('releaseUI.main', ['ngRoute', 'ngMaterial']);

app.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/', {
    templateUrl: 'main/main.html',
    controller: 'MainController'
  });
}]);

app.controller('MainController', function($scope, $http, $log) {

    // Get information from http request
    var labelSet = new Set();
    var labels;
    $http({
      method: 'GET',
      url: '/fake_data.json',
      cache: true
    }).then(function successCallback(response) {
      releases = angular.fromJson(response.data);
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
      {"id":0, "status": "Status"},
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
});

// Filter on all properties
app.filter('propFilter', function($log) {
  return function(items, state, label, from, to, which) {

    //filter based on created dates
    var filteredDate = [];
    angular.forEach(items, function (item) {
      var time;
      if(which == 'started'){
        time = item.started * 1000;
      }
      else{
        time = item.last_modified * 1000;
      }
      if (time >= from && time <= to){
        filteredDate.push(item);
      }
    })

    //filter based on state
    var filteredState = [];
    if (state == null) {
      filteredState = items;
    }
    else {
      angular.forEach(items, function (item) {
        if (item.state == state){
          filteredState.push(item);
        }
      })
    }

    //filter based on label
    var filteredLabel = [];
    if (label == null) {
      filteredLabel = items;
    }
    else {
      angular.forEach(items, function (item) {
        for(var i = 0; i < item.labels.length; i++){
          if (item.labels[i] == label){
            filteredLabel.push(item);
          }
        }
      })
    }

    // return intersection of arrays
    return intersection(filteredDate, filteredLabel, filteredState);
  }
});

// OrderBy function for dictionary instead of array
app.filter('orderObjectBy', function() {
  return function(items, field, reverse) {
    var filtered = [];
    angular.forEach(items, function(item) {
      filtered.push(item);
    });
    filtered.sort(function (a, b) {
      return (a[field] > b[field] ? 1 : -1);
    });
    if(reverse) filtered.reverse();
    return filtered;
  };
});

// intersection of arrays
function intersection() {
  var result = [];
  var lists;

  if(arguments.length === 1) {
    lists = arguments[0];
  } else {
    lists = arguments;
  }

  for(var i = 0; i < lists.length; i++) {
    var currentList = lists[i];
    for(var y = 0; y < currentList.length; y++) {
        var currentValue = currentList[y];
      if(result.indexOf(currentValue) === -1) {
        var existsInAll = true;
        for(var x = 0; x < lists.length; x++) {
          if(lists[x].indexOf(currentValue) === -1) {
            existsInAll = false;
            break;
          }
        }
        if(existsInAll) {
          result.push(currentValue);
        }
      }
    }
  }
  return result;
}
