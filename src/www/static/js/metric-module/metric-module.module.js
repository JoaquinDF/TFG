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


    $scope.isobj = function (a) {
        return (angular.isObject(a))
    }


}]);

mlist.controller('MAPS', ['$scope', '$http', function ($scope, $http) {
    $scope.nodeinfo = [];

    $scope.mapObject = function (what) {

        var mapdata = {}
        var dataseries = []
        var apiget = '/api/v1/data/RegionMetricToPairDict/'
        var setobject = {
            "?": what
        }
        document.getElementById('container').innerHTML = "";
        document.getElementById('container').style.display = "block";
        document.getElementById('sigma-container').style.display = "none";
        var nodeinfo = document.getElementsByClassName('nodeinfo');
        for (var x in nodeinfo.length) {
            nodeinfo[x].hidden = "true";
        }

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


    }


    $scope.reloadinfoonclick = function (info) {
        debugger;
        $scope.nodeinfo = info;
        var arraydata = info.split(" ");
        var infoinside = "<h3>"
        for (var data in arraydata) {
            debugger;

            infoinside += '<br>' + arraydata[data]
        }
        infoinside += "</h3>"

        document.getElementById("nodeinfo").innerHTML = infoinside;
        document.getElementById("nodeinfo").style.background = "rgba(24, 82, 242, 0.21)"


    }

    $scope.reloadinfoonhover = function (info) {
        debugger;
        $scope.nodeinfo = info;
        var arraydata = info.split(" ");

        var infoinside = "<h3>"
        for (var data in arraydata) {
            debugger;

            infoinside += '<br>' + arraydata[data]
        }
        infoinside += "</h3>"

        document.getElementById("nodeinfohover").innerHTML = infoinside;
        document.getElementById("nodeinfohover").style.background = "rgba(91, 16, 30, 0.21)";
        var nodeinfo = document.getElementsByClassName('nodeinfo');
        for (var x in nodeinfo.length) {
            nodeinfo[x].hidden = "false";
        }
    }

    $scope.communityObject = function () {
        document.getElementById('container').style.display = "none";
        document.getElementById('sigma-container').style.display = "block";
        document.getElementById('sigma-container').innerHTML = "";


        try {
            sigma.classes.graph.addMethod('neighbors', function (nodeId) {
                var k,
                    neighbors = {},
                    index = this.allNeighborsIndex[nodeId] || {};

                for (k in index)
                    neighbors[k] = this.nodesIndex[k];

                return neighbors;
            });
        } catch (err) {
            ;
        }


        sigma.parsers.json('/api/v1/test-files/gexf/', {
                container: 'sigma-container',
                renderer: {container: document.getElementById('sigma-container'), type: 'canvas'},
                settings: {
                    maxNodeSize: 30,
                    minEdgeSize: 2,
                    maxEdgeSize: 2,
                    minArrowSize: 25,
                    labelThreshold: 1,
                    defaultLabelSize: 25,

                }

            },

            function (sigmaInstance) {
                sigmaInstance.graph.nodes().forEach(function (node, i, a) {
                    node.x = Math.cos(Math.PI * 2 * i / a.length);
                    node.y = Math.sin(Math.PI * 2 * i / a.length);
                });
                sigmaInstance.refresh();
                sigmaInstance.startForceAtlas2({
                    worker: true,
                    barnesHutOptimize: false,
                    scalingRatio: 500,
                    gravity: 0
                });

                setTimeout(function () {
                    sigmaInstance.stopForceAtlas2();
                }, 3000);

                sigmaInstance.graph.nodes().forEach(function (n) {
                    n.originalColor = n.color;
                });
                sigmaInstance.graph.edges().forEach(function (e) {
                    e.originalColor = e.color;
                });


                sigmaInstance.bind('clickNode', function (e) {

                    var nodeId = e.data.node.id,
                        toKeep = sigmaInstance.graph.neighbors(nodeId);
                    toKeep[nodeId] = e.data.node;
                    $scope.nodeinfo = e.data.node.info.split(' ');
                    $scope.reloadinfoonclick(e.data.node.info);

                    sigmaInstance.graph.nodes().forEach(function (n) {
                        if (toKeep[n.id]) {
                            n.color = n.originalColor;
                            e.data.node.color = '#1954f2'
                        }
                        else
                            n.color = 'rgba(198, 36, 63, 0.26)';
                    });

                    sigmaInstance.graph.edges().forEach(function (e) {
                        if (toKeep[e.source] && toKeep[e.target])
                            e.color = e.originalColor;
                        else
                            e.color = 'rgba(198, 36, 63, 0.1)';
                    });

                    // Since the data has been modified, we need to
                    // call the refresh method to make the colors
                    // update effective.
                    sigmaInstance.refresh();


                });
                sigmaInstance.bind('overNode', function (e) {

                    $scope.reloadinfoonhover(e.data.node.info);


                });


            });


    }
    $scope.debug = function (a) {
        debugger;

    }

}]);


mlist.controller('Chart', ['$scope', function ($scope) {
    $scope.optionspie = {
        tooltips: {bodyFontSize: 15, titleFontSize: 10},
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
    $scope.optionspolar = {
        tooltips: {
            bodyFontSize: 15, titleFontSize: 10,


        },
        responsive: true,
        maintainAspectRatio: true,
        display: true,
        legend: {
            display: false,
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

