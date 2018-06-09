'use strict';
var releases;
var labels;

angular.module('releaseUI.main', ['ngRoute', 'ngMaterial'])
.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/', {
    templateUrl: 'main/main.html',
    controller: 'MainController'
  });
}]);

App.controller('MainController', function($scope, $cacheFactory, $http, $log) {
    labels = new Set();
    $http({
      method: 'GET',
      url: 'fake_data.json',
      cache: true
    }).then(function successCallback(response) {
      releases = angular.fromJson(response.data);
      angular.forEach(releases, function(value, key) {
        for (var i = 0; i < value.labels.length; i++) {
          labels.add(value.labels[i]);
        }
      })
      $scope.releases = releases;
      $scope.labels = Array.from(labels);
    }, function errorCallback(response) {
      $log.log(response);
    });

    $scope.stateValues = [
      {"id":0, "status": "Status"},
      {"id":1, "status": "Finished"},
      {"id":2, "status": "Failed"},
      {"id":3, "status": "Pending"},
      {"id":4, "status": "Suspended"},
    ];

    $scope.selected = $scope.stateValues[0];
    $scope.stateValue = 0;
    $scope.hasChanged = function(state) {
      $log.log($scope.selected.id);
      $scope.stateValue = $scope.selected.id;
    };
});

App.controller('StatusController', function($scope) {
  $scope.statusList = [
    {"id":0, "status": "Status"},
    {"id":1, "status": "Finished"},
    {"id":2, "status": "Failed"},
    {"id":3, "status": "Pending"},
    {"id":4, "status": "Suspended"},
  ];
});

App.controller('LabelController', function($scope) {

});

// Filter depending on selected state (state == 0 shows all)
App.filter('stateFilter', function() {
  return function(input, state) {
    var output = [];

    if (state == 0) {
      output = input;
    }
    else {
      angular.forEach(input, function (item) {
        if (item == state){
          output.push(item);
        }
      })
    }
    return output;
  }
});

// OrderBy function for dictionary instead of array
App.filter('orderObjectBy', function() {
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
