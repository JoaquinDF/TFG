'use strict';

// Define the `projectList` module
var mlist = angular.module('metricModule', ["chart.js", 'ngMaterial']);

mlist.controller('LOAD', ['$scope', '$window', function ($scope, $window) {
    $scope.onURLclick = function (url1, url2) {
        var url = "/www/#!" + url1 + url2
        debugger;

        $window.location.href = url
    }
}])


mlist.controller('DEBUG', ['$scope', function ($scope) {

    $scope.debug = function (a, b) {


    }

    $scope.isobj = function (a) {
        return (angular.isObject(a))
    }


}]);

mlist.controller('Chart', ['$scope', function ($scope) {
    $scope.optionspie = {
        tooltips: {bodyFontSize: 20, titleFontSize: 15},
        responsive: true,
        maintainAspectRatio: true,
        display: true,
        legend: {
            display: true,
            labels: {
                fontSize: 20,

            }
        },

    };

    $scope.optionsbar = {
        tooltips: {bodyFontSize: 20, titleFontSize: 15},
        responsive: true,
        legend: {
            display: true,
            labels: {

                fontSize: 20,
            }
        },
        scales: {
            yAxes: [{
                display: true,
                ticks: {
                    suggestedMin: 30
                }
            }]
        }
    };
    $scope.mapObject = {
        scope: 'usa',
        options: {
            width: 1110,
            legendHeight: 60 // optionally set the padding for the legend
        },
        geographyConfig: {
            highlighBorderColor: '#EAA9A8',
            highlighBorderWidth: 2
        },
        fills: {
            'HIGH': '#CC4731',
            'MEDIUM': '#306596',
            'LOW': '#667FAF',
            'defaultFill': '#DDDDDD'
        },
        data: {
            "AZ": {
                "fillKey": "MEDIUM",
            },
            "CO": {
                "fillKey": "HIGH",
            },
            "DE": {
                "fillKey": "LOW",
            },
            "GA": {
                "fillKey": "MEDIUM",
            }
        },
    }

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

