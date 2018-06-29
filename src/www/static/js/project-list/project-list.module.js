'use strict';
/**
 * Modululo principal de las convocatorias
 * @namespace innhomeweb.Project-list-Module
 */
// Define the `projectList` module
var plist = angular.module('projectList', ['ngRoute']);


plist //return the data filtered
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






