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
