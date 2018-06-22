'use strict';

var app = angular.module('ReleaseUI.services', ['ngResource']);

app.factory('serviceRelease', function() {
  var savedData = {};
  function set(data){
    savedData = data;
  }
  function get() {
    return savedData;
  }

  return {
    set: set,
    get: get
  };
});

//app.factory('authService', function ($firebaseAuth, cityTimerService) {
//   var firebaseAuthObject = $firebaseAuth();
//   var service = {
//      firebaseAuthObject: firebaseAuthObject,
//      login: login,
//      logout: logout,
//      isLoggedIn: isLoggedIn,
//   };
//   return service;
//
//   function login() {
//     var provider = new firebase.auth.GithubAuthProvider();
//     firebase.auth().signInWithRedirect(provider)
//     .then(function(result) {
//        return result.user;
//       $log.log(result.user);
//     }).catch(function(error) {
//        var errorCode = error.code;
//        var errorMessage = error.message;
//
//        $log.log(errorCode);
//        $log.log(errorMessage);
//     });
//   }
//
//   function logout() {
//      cityTimerService.reset();
//      firebaseAuthObject.$signOut();
//   }
//   function isLoggedIn() {
//      return firebaseAuthObject.$getAuth();
//   }
//});
