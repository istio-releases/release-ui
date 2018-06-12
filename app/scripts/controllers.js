'use strict';

/* Controllers */

var app = angular.module('ReleaseUI.controllers', []);

app.controller('MainController', function($scope, $http, $location, $log) {

    // Get information from http request
    var labelSet = new Set();
    var labels;
    $http({
      method: 'GET',
      url: '/app/scripts/fake_data.json',
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

    // Redirect to Details function
    $scope.redirectToDetails = function (input) {
      $log.log(input);
      $location.path('/details').search('release', input);
    }
});

var data = {
  "artifacts_link": "https://youtu.be/dQw4w9WgXcQ",
  "tasks": {
    "task2_ID": {
      "status": 1,
      "log_url": "https://youtu.be/dQw4w9WgXcQ",
      "started": 2050109653,
      "dependent_on": [
        "task0_ID",
        "task1_ID"
      ],
      "last_modified": 1641373703,
      "task_name": "task-2",
      "error": "error number 194"
    },
    "task4_ID": {
      "status": 1,
      "log_url": "https://youtu.be/dQw4w9WgXcQ",
      "started": 1412095131,
      "dependent_on": [
        "task0_ID",
        "task1_ID",
        "task2_ID",
        "task3_ID"
      ],
      "last_modified": 1663161257,
      "task_name": "task-4",
      "error": "error number 126"
    },
    "task1_ID": {
      "status": 4,
      "log_url": "https://youtu.be/dQw4w9WgXcQ",
      "started": 173883905,
      "dependent_on": [
        "task0_ID"
      ],
      "last_modified": 7895027,
      "task_name": "task-1",
      "error": "error number 804"
    },
    "task3_ID": {
      "status": 3,
      "log_url": "https://youtu.be/dQw4w9WgXcQ",
      "started": 2044718921,
      "dependent_on": [
        "task0_ID",
        "task1_ID",
        "task2_ID"
      ],
      "last_modified": 561944342,
      "task_name": "task-3",
      "error": "error number 203"
    },
    "task0_ID": {
      "status": 1,
      "log_url": "https://youtu.be/dQw4w9WgXcQ",
      "started": 1390238018,
      "dependent_on": [],
      "last_modified": 1558698276,
      "task_name": "task-0",
      "error": "error number 919"
    }
  },
  "name": "release-6",
  "release_url": "https://youtu.be/dQw4w9WgXcQ",
  "started": 1003393974,
  "labels": [
    "label0",
    "label1",
    "label2"
  ],
  "state":3,
  "last_modified": 1528490634,
  "repo_url": "https://youtu.be/dQw4w9WgXcQ",
  "last_active_task": "task1_ID",
  "ref": "reference number 780",
  "stage": 4};

app.controller('DetailsController', function ($scope) {
  $scope.release = data;
});
