'use strict';

// Define the `projectList` module
var olist = angular.module('organizationList', []);


olist //return the data filtered
    .filter('custom', function () {
        return function (input, search) {
            var success;
            success = false;

            if (!input) return input;
            if (!search) return input;
            var expected = ('' + search).toLowerCase();
            var result = {};
            angular.forEach(input, function (value, key) {
                var actual = ('' + value).toLowerCase();
                if (actual.indexOf(expected) !== -1) {
                    success = true;

                }
            });
            if (success == true) {
                angular.forEach(input, function (value, key) {
                    result[key] = value;

                });

                success = false;
                return result;
            }
            ;


            return result;
        }
    });

olist.controller('Ctrl', ['$scope', function ($scope) {
    $scope.isobj = function (a) {
        if (angular.isObject(a)) {
            angular.forEach(a, function (value, key) {
                console.log("Key= " + value + " Value= " + key);

            });
        }
        return angular.isObject(a);

    }
    $scope.debug = function (a, b) {
        console.log("Key= " + a + " Value= " + b);
        debugger;

    }
}]);





