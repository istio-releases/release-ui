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
  }
});

app.factory('serviceReleaseList', function () {
  var releaseList = [];
  function set(data){
    releaseList = data;s
  }
  function get(){
    return releaseList;
  }

  return {
    set: set,
    get: get
  }
});

app.factory('authService', function ($firebaseAuth, firebaseDataService, cityTimerService) {
   var firebaseAuthObject = $firebaseAuth();
   var service = {
      firebaseAuthObject: firebaseAuthObject,
      register: register,
      login: login,
      logout: logout,
      isLoggedIn: isLoggedIn,
      sendWelcomeEmail: sendWelcomeEmail
   };
   return service;

   ////////////
   function register(user) {
      return firebaseAuthObject.$createUserWithEmailAndPassword(user.email, user.password);
   }
   function login(user) {
      return firebaseAuthObject.$signInWithEmailAndPassword(user.email, user.password);
   }
   function logout() {
      cityTimerService.reset();
      firebaseAuthObject.$signOut();
   }
   function isLoggedIn() {
      return firebaseAuthObject.$getAuth();
   }
   function sendWelcomeEmail(emailAddress) {
      firebaseDataService.emails.push({
          emailAddress: emailAddress
      });
   }
});
