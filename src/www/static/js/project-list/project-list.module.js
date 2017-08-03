'use strict';

// Define the `projectList` module
var plist = angular.module('projectList', []);

plist.filter('myFilter', function () {
    return function (items, search) {
        var result = [];
        angular.forEach(items, function (value, key) {
            angular.forEach(value, function (value2, key2) {
                if (value2 === search) {
                    result.push(value2);
                }
            })
        });
        return result;

    }
});