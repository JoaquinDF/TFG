'use strict';

// Define the `projectList` module
var mlist = angular.module('metricModule', ["chart.js"]);


mlist.controller('DEBUG', ['$scope', function ($scope) {

    $scope.debug = function (a, b) {


    }

    $scope.isobj = function (a) {
        return (angular.isObject(a))
    }


}]);


mlist.filter('custom', function () {
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

mlist.controller('GraphPlot', ['$scope', '$interval', '$rootScope', function ($scope, $interval, $rootScope) {

    var plot = false;
    var isnan = $interval(function () {
        if (!isNaN($rootScope.averagesubvencionado)) {

            $interval.cancel(isnan);
            plot = true
        }
        $scope.labels = ["Presupuesto Subvencionado - %", "Presupuesto sin Subvencionar - %"];
        $scope.data = [$rootScope.averagesubvencionado, (100 - $rootScope.averagesubvencionado)];
    }, 1000);


}]);