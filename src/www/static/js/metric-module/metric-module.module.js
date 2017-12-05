'use strict';

// Define the `projectList` module
var mlist = angular.module('metricModule', ["chart.js", 'ngMaterial']);

mlist.controller('LOAD', ['$scope', '$window', function ($scope, $window) {
    $scope.onURLclick = function (url1, url2) {
        var url = "/www/#!" + url1 + url2

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

mlist.controller('MAPS', ['$scope', '$http', function ($scope, $http) {
    $scope.mapObject = function (what) {

        var mapdata = {}
        var dataseries = []
        var apiget = '/api/v1/data/RegionMetricToPairDict/'
        var setobject = {
            "?": what
        }
        document.getElementById('container').innerHTML = "";


        $http.post(apiget, setobject).then(function successCallback(response) {
            debugger;
            dataseries = response.data;


            var onlyValues = dataseries.map(function (obj) {
                return obj[1];
            });

            var minValue = Math.min.apply(null, onlyValues),
                maxValue = Math.max.apply(null, onlyValues);

            var paletteScale = d3.scale.linear()
                .domain([minValue, maxValue])
                .range(["#FFFFFF", "#5a101d"]);
            debugger;
            dataseries.forEach(function (item) { //
                // item example value ["USA", 70]
                var iso = item[0],
                    value = item[1].toFixed(1);
                mapdata[iso] = {numberOfThings: value, fillColor: paletteScale(value)};

            });
            debugger;

            var map = new Datamap({

                element: document.getElementById('container'),

                scope: 'world',


                fills: {defaultFill: '#F5F5F5'},
                data: $scope.debug(mapdata),

                // Zoom in on EUROPE
                setProjection: function (element) {
                    var projection = d3.geo.mercator()
                        .center([-15, 56])
                        .scale(615)
                        .translate([element.offsetWidth / 2, element.offsetHeight / 2]);
                    var path = d3.geo.path()
                        .projection(projection);


                    return {path: path, projection: projection};
                },
                geographyConfig: {
                    borderColor: '#DEDEDE',
                    highlightBorderWidth: 2,
                    // don't change color on mouse hover
                    highlightFillColor: function (geo) {
                        return geo['fillColor'] || '#F5F5F5';
                    },
                    // only change border
                    highlightBorderColor: '#B7B7B7',
                    // show desired information in tooltip
                    popupTemplate: function (geo, mapdata) {
                        debugger;
                        // don't show tooltip if country don't present in dataset
                        if (!mapdata) {
                            return;
                        }
                        // tooltip content
                        return ['<div class="hoverinfo">',
                            '<strong>', geo.properties.name, '</strong>',
                            '<br>Count: <strong>', mapdata.numberOfThings, '</strong>',
                            '</div>'].join('');
                    }
                }


            });


        });

        /*var series = [
         ["BLR",75],["BLZ",43],["RUS",50],["RWA",88],["SRB",21],["TLS",43],
         ["REU",21],["TKM",19],["TJK",60],["ROU",4],["TKL",44],["GNB",38],
         ["GUM",67],["GTM",2],["SGS",95],["GRC",60],["GNQ",57],["GLP",53],
         ["JPN",59],["GUY",24],["GGY",4],["GUF",21],["GEO",42],["GRD",65],
         ["GBR",14],["GAB",47],["SLV",15],["GIN",19],["GMB",63],["GRL",56],
         ["ERI",57],["MNE",93],["MDA",39],["MDG",71],["MAF",16],["MAR",8],
         ["MCO",25],["UZB",81],["MMR",21],["MLI",95],["MAC",33],["MNG",93],
         ["MHL",15],["MKD",52],["MUS",19],["MLT",69],["MWI",37],["MDV",44],
         ["MTQ",13],["MNP",21],["MSR",89],["MRT",20],["IMN",72],["UGA",59],
         ["TZA",62],["MYS",75],["MEX",80],["ISR",77],["FRA",54],["IOT",56],
         ["SHN",91],["FIN",51],["FJI",22],["FLK",4],["FSM",69],["FRO",70],
         ["NIC",66],["NLD",53],["NOR",7],["NAM",63],["VUT",15],["NCL",66],
         ["NER",34],["NFK",33],["NGA",45],["NZL",96],["NPL",21],["NRU",13],
         ["NIU",6],["COK",19],["XKX",32],["CIV",27],["CHE",65],["COL",64],
         ["CHN",16],["CMR",70],["CHL",15],["CCK",85],["CAN",76],["COG",20],
         ["CAF",93],["COD",36],["CZE",77],["CYP",65],["CXR",14],["CRI",31],
         ["CUW",67],["CPV",63],["CUB",40],["SWZ",58],["SYR",96],["SXM",31]];





         var dataset = {};


         var onlyValues = series.map(function(obj){ return obj[1]; });
         var minValue = Math.min.apply(null, onlyValues),
         maxValue = Math.max.apply(null, onlyValues);


         var paletteScale = d3.scale.linear()
         .domain([minValue,maxValue])
         .range(["#EFEFFF","#02386F"]);

         series.forEach(function(item){

         var iso = item[0],
         value = item[1];
         dataset[iso] = { numberOfThings: value, fillColor: paletteScale(value) };
         });

         new Datamap({
         element: document.getElementById('container'),
         projection: 'mercator',

         fills: { defaultFill: '#F5F5F5' },
         data: dataset,
         geographyConfig: {
         borderColor: '#DEDEDE',
         highlightBorderWidth: 2,


         highlightFillColor: function(geo) {
         return geo['fillColor'] || '#F5F5F5';
         },

         highlightBorderColor: '#B7B7B7',

         popupTemplate: function(geo, data) {

         if (!data) { return ; }

         return ['<div class="hoverinfo">',
         '<strong>', geo.properties.name, '</strong>',
         '<br>Count: <strong>', data.numberOfThings, '</strong>',
         '</div>'].join('');
         }
         }
         });
         */
    }
    $scope.debug = function (entrada) {
        debugger;
        return entrada;
    }
}])

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

