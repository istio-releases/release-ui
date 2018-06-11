'use strict';

app = angular.module('releaseUI.details', ['ngRoute']);

app.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/details', {
    templateUrl: 'details/details.html',
    controller: 'DetailsController'
  });
}]);

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

app.controller('DetailsController', function($scope) {
  $scope.release = data;
});
