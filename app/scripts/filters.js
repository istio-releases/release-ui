'use strict';

/* Filters */

var app = angular.module('ReleaseUI.filters', []);

// Filter on all properties
app.filter('propFilter', function() {
  return function(items, state, label, from, to, which) {

    //filter based on created dates
    var filteredDate = [];
    angular.forEach(items, function (item) {
      var time;
      if(which == 'started'){
        time = item.started * 1000;
      }
      else{
        time = item.last_modified * 1000;
      }
      if (time >= from && time <= to){
        filteredDate.push(item);
      }
    })

    //filter based on state
    var filteredState = [];
    if (state == null) {
      filteredState = items;
    }
    else {
      angular.forEach(items, function (item) {
        if (item.state == state){
          filteredState.push(item);
        }
      })
    }

    //filter based on label
    var filteredLabel = [];
    if (label == null) {
      filteredLabel = items;
    }
    else {
      angular.forEach(items, function (item) {
        for(var i = 0; i < item.labels.length; i++){
          if (item.labels[i] == label){
            filteredLabel.push(item);
          }
        }
      })
    }

    // return intersection of arrays
    return intersection(filteredDate, filteredLabel, filteredState);
  }
});

// OrderBy function for dictionary instead of array
app.filter('orderObjectBy', function() {
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

// intersection of arrays
function intersection() {
  var result = [];
  var lists;

  if(arguments.length === 1) {
    lists = arguments[0];
  } else {
    lists = arguments;
  }

  for(var i = 0; i < lists.length; i++) {
    var currentList = lists[i];
    for(var y = 0; y < currentList.length; y++) {
        var currentValue = currentList[y];
      if(result.indexOf(currentValue) === -1) {
        var existsInAll = true;
        for(var x = 0; x < lists.length; x++) {
          if(lists[x].indexOf(currentValue) === -1) {
            existsInAll = false;
            break;
          }
        }
        if(existsInAll) {
          result.push(currentValue);
        }
      }
    }
  }
  return result;
}

app.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);
    for (var i=0; i<total && i < 3; i++)
      input.push(i-1);
    return input;
  };
});
