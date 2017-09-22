'use strict';

// Define the `projectList` module
var transform = angular.module('transformModule', []);

transform.filter('person', [function () {
    return function (object) {

        var array = [];
        angular.forEach(object, function (key, value) {

            if (value.indexOf('person') == -1)
                array.push(value);
        });
        debugger;
        return array;
    };
}]);
