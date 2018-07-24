'use strict';

/* Filters */

var app = angular.module('ReleaseUI.filters', []);


app.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);
    for (var i=0; i<total && i < 3; i++)
      input.push(i-1);
    return input;
  };
});
