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
    var labelSet = new Set();
    var labels;
    $http({
      method: 'GET',
      url: 'fake_data.json',
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

    // Starting settings for label filtered
    $scope.labelValue = 'all';

    // Starting settings for search filter
    $scope.searchTable = undefined;

    // Starting settings for state filter
    $scope.selectedValue = 0;
    $scope.stateValues = [
      {"id":0, "status": "Status"},
      {"id":2, "status": "Finished"},
      {"id":3, "status": "Failed"},
      {"id":1, "status": "Pending"},
      {"id":4, "status": "Suspended"},
    ];
    $scope.stateValue = 0;

    // Starting Settings for OrderBy filter
    $scope.sortType = 'last_modified';
    $scope.sortReverse = true;
});

app.controller('LabelController', function($scope) {

});

// Filter depending on selected state (state == 0 shows all)
app.filter('stateFilter', function() {
  return function(items, state) {
    var filtered = [];
    if (state == 0) {
      filtered = items;
    }
    else {
      angular.forEach(items, function (item) {
        if (item.state == state){
          filtered.push(item);
        }
      })
    }
    return filtered;
  }
});

// Filter depending on selected label
app.filter('propFilter', function($log) {
  return function(items, state, label) {

    //filter based on state
    var filteredState = [];
    if (state == 0) {
      filteredState = items;
    }
    else {
      angular.forEach(items, function (item) {
        if (item.state == state){
          filteredState.push(item);
        }
      })
    }

    // filter based on label
    var filteredLabel = [];
    if (label == 'all') {
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
    return filteredState.filter(value => -1 !== filteredLabel.indexOf(value));
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
