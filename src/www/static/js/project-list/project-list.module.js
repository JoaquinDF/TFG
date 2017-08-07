'use strict';

// Define the `projectList` module
var plist = angular.module('projectList', []);


plist //return the data filtered
.filter('custom', function() {
  return function(input, search) {
  var success;
  success = false;

    if (!input) return input;
    if (!search) return input;
    var expected = ('' + search).toLowerCase();
    var result = {};
    angular.forEach(input, function(value, key) {
      var actual = ('' + value).toLowerCase();
      if (actual.indexOf(expected) !== -1) {
        success = true;
        debugger;
      }
    });
    if(success==true){
      angular.forEach(input, function(value, key) {
        result[key] = value;

      });

       success=false;
        return result;
    };


      return result;
  }
});






