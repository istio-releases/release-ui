var fake1 = {"version":"xxx-xxx-123","status":1,"creation":"01 Jan 1970 00:00:00","last_mod":"01 Jan 1970 00:00:00","last_active":"task123","tags":[1,3]}
var fake2 = {"version":"xxx-xxx-456","status":2,"creation":"04 Dec 2017 00:12:00","last_mod":"04 Dec 2017 00:12:00","last_active":"task456","tags":[2]}
var fake3 = {"version":"xxx-xxx-789","status":3,"creation":"29 Jun 1999 4:30:30","last_mod":"29 Jun 1999 4:30:30","last_active":"task789","tags":[4]}
var fake4 = {"version":"xxx-xxx-000","status":4,"creation":"04 Dec 1995 00:12:00","last_mod":"04 Dec 1995 00:12:00","last_active":"task000","tags":[1,2]}
var fakeData = [fake1, fake2, fake3, fake4]

App.controller('MainController', function($scope) {
  $scope.releases = fakeData;
});
