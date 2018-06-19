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
    releaseList = data;
  }
  function get(){
    return releaseList;
  }

  return {
    set: set,
    get: get
  }
});

app.factory('PersistentData','$log', function () {
  var savedData = {};

  // Starting settings for
  savedData.currentPage = 1;

  savedData.ChangeCurrentPage = function (value) {
    savedData.currentPage = value;
  };

  return savedData

});
