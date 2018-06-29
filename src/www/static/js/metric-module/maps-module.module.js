'use strict';
/**
 * Controlador principal de los Mapas de Calor
 * @namespace innhomeweb.Community-Maps
 */
angular.module('mapsModule', []).controller('ControladorMaps', ['$scope', '$http', '$routeParams', function ($scope, $http, $routeParams) {

    var what = $routeParams.map

    var mapdata = {}
    var dataseries = []
    var apiget = '/api/v1/data/RegionMetricToPairDict/'
    var setobject = {
        "?": what
    }


    $scope.tabcolor = function (id) {


        var i;
        var x = document.getElementsByClassName("tablink");
        for (i = 0; i < x.length; i++) {
            x[i].style.background = 'none';
            x[i].style.color = '#ffffff';

        }
        document.getElementById(id).style.background = '#ccc';
        document.getElementById(id).style.color = '#000000';


    }

    /**
     * Crea los distintos mapas dependiendo el JSON de entrada
     * @memberof innhomeweb.Community-Maps
     * @method Createmaps
     * @param {JSON} data Indica los datos que va a cargar sobre el mapa
     */
    document.getElementById('container').innerHTML = "";

    $http.post(apiget, setobject).then(function successCallback(response) {
        dataseries = response.data;

        var onlyValues = dataseries.map(function (obj) {
            return obj[1];
        });

        var minValue = Math.min.apply(null, onlyValues),
            maxValue = Math.max.apply(null, onlyValues);

        var paletteScale = d3.scale.linear()
            .domain([minValue, maxValue])
            .range(["#FFFFFF", "#5a101d"]);
        dataseries.forEach(function (item) { //
            // item example value ["USA", 70]
            var iso = item[0],
                value = item[1].toFixed(1);
            mapdata[iso] = {numberOfThings: value, fillColor: paletteScale(value)};

        });

        var map = new Datamap({

            element: document.getElementById('container'),

            scope: 'world',


            fills: {defaultFill: '#F5F5F5'},
            data: mapdata,

            // Zoom in on EUROPE
            setProjection: function (element) {
                var projection = d3.geo.mercator()
                    .center([13, 52])
                    .scale([element.offsetWidth / 1.5])
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


}]);
