'use strict';

var mlist = angular.module('metricModule', ["chart.js", 'ngMaterial']);

mlist.controller('LOAD', ['$scope', '$window', function ($scope, $window) {
    $scope.onURLclick = function (url1, url2) {
        var url = "/www/#!" + url1 + url2

        $window.location.href = url
    }
}])


mlist.controller('DEBUG', ['$scope', function ($scope) {


    $scope.isobj = function (a) {
        return (angular.isObject(a))
    }


}]);


mlist.controller('Chart', ['$scope', function ($scope) {
    $scope.optionspie = {


        responsive: true,
        maintainAspectRatio: true,
        display: true,
        legend: {
            display: true,
            position: "bottom"

        },

    };
    $scope.optionspolar = {
        responsive: true,
        maintainAspectRatio: true,
        display: true,
        legend: {
            display: false,
            position: "bottom"


        },


    };

    $scope.optionsbar = {

        responsive: true,
        maintainAspectRatio: true,
        display: true,
        legend: {
            display: true,
            position: "bottom"

        },
    };


}])

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

