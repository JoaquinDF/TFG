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

                if (angular.isObject(value)) {
                    angular.forEach(value, function (valueinner, keyinner) {
                        var actual = ('' + valueinner).toLowerCase();
                        if (actual.indexOf(expected) !== -1) {
                            success = true;

                        }
                    });

                } else {

                    var actual = ('' + value).toLowerCase();
                    if (actual.indexOf(expected) !== -1) {
                        success = true;

                    }
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
        return angular.isObject(a);

    }
    $scope.debug = function (a, b) {

    }
}]);






