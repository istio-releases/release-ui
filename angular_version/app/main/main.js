'use strict';
var releases;

angular.module('releaseUI.main', ['ngRoute', 'ngMaterial'])
.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/', {
    templateUrl: 'main/main.html',
    controller: 'MainController'
  });
}]);

App.controller('MainController', function($scope, $cacheFactory, $http) {
    $http({
      method: 'GET',
      url: '/fake_data.json',
      cache: true
    }).then(function successCallback(response) {
      $scope.releases = angular.fromJson(response.data);
      releases = angular.fromJson(response.data);
    }, function errorCallback(response) {
      $log.log(response);
    });
});

App.controller('StatusController', function($scope) {
  $scope.statusList = [
    {"id":0, "status": "Status"},
    {"id":1, "status": "Finished"},
    {"id":2, "status": "Failed"},
    {"id":3, "status": "Pending"},
    {"id":4, "status": "Suspended"},
  ];

  $scope.statusChange = function () {
    filterStatus = $scope.statusValue;
    $scope.$emit('filtered');
  };

});

App.controller('LabelController', function($scope) {
  
});

App.filter('statusFilter', function() {
  return function(input, status) {

    var output = [];

    if (status == 0) {
      output = input;
    }
    else {
      angular.forEach(input, function (item) {
        if (item.status == status){
          output.push(item);
        }
      })
    }
    return output;
  }
});
