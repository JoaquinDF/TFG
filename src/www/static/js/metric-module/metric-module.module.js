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

mlist.controller('MAPS', ['$scope', '$http', '$cacheFactory', function ($scope, $http, $cacheFactory) {
    try {
        console.log("cache")
        $scope.cache = $cacheFactory('c1');
    }
    catch (err) {
        console.log('Intancia de Cache ya creada')
    }
    $scope.nodeinfo = [];

    $scope.showwordcloud = function (value) {
        if (value) {
            document.getElementById('wordcloud').style.display = ""
            document.getElementById('projectid').style.display = "none"


            $scope.wordcloud = value

        } else {
            document.getElementById('wordcloud').style.display = "none"
            document.getElementById('projectid').style.display = ""

            $scope.wordcloud = value


        }

    }
    $scope.mapObject = function (what) {
        $scope.wordcloud = false;
        $scope.showwordcloud(false)
        var mapdata = {}
        var dataseries = []
        var apiget = '/api/v1/data/RegionMetricToPairDict/'
        var setobject = {
            "?": what
        }
        document.getElementById('container').innerHTML = "";
        document.getElementById('container').style.display = "";
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


    };

    $scope.drawWordCloud = function (text, svglocation) {


        var word_count = {};

        var words = [];

        text.forEach(function (word) {
            try {
                var splited = word.split(' ')
                var word = splited[1].toLowerCase();
                word_count[word] = parseFloat(splited[2]);

            } catch (err) {
            }
        })


        var svg_location = svglocation;
        var width = 400;
        var height = 300;

        var fill = d3.scale.category20();

        var word_entries = d3.entries(word_count);

        var xScale = d3.scale.log()
            .domain([d3.min(word_entries, function (d) {
                return d.value;
            }), d3.max(word_entries, function (d) {
                return d.value;
            })
            ])
            .range([20, 150]);

        d3.layout.cloud().size([width, height])
            .timeInterval(20)
            .words(word_entries)
            .fontSize(function (d) {
                return xScale(+d.value);
            })
            .text(function (d) {
                return d.key;
            })
            .rotate(function () {
                return ~~(Math.random() * 2) * 90;
            })
            .font("Impact")
            .on("end", draw)
            .start();

        function draw(words) {
            d3.select(svg_location).append("svg")
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", "translate(" + [width >> 1, height >> 1] + ")")
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", function (d) {
                    return xScale(d.value) + "px";
                })
                .style("font-family", "Impact")
                .style("fill", function (d, i) {
                    return fill(i);
                })
                .attr("text-anchor", "middle")
                .attr("transform", function (d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function (d) {
                    return d.key;
                });
        }

        $scope.previousdata = text;
        d3.layout.cloud().stop();
    };


    $scope.reloadinfoonclick = function (info) {


        document.getElementById("nodeinfo").innerHTML = "";

        var arraydata = info.split(",");
        $scope.drawWordCloud(arraydata, '#nodeinfo')


    };

    $scope.reloadinfoonhover = function (info) {

        document.getElementById("nodeinfohover").innerHTML = "";

        var arraydata = info.split(",");
        $scope.drawWordCloud(arraydata, '#nodeinfohover')


    };

    $scope.communityObject = function (datajson) {
        document.getElementById('container').style.display = "none";
        document.getElementById('sigma-container').style.display = "block";
        document.getElementById('sigma-container').innerHTML = ""

        var a = parseInt(datajson)
        if (isNaN(a)) {
            $scope.showwordcloud(true)
        } else {
            $scope.showwordcloud(false)


        }


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

        var apicall = '/api/v1/test-files/' + datajson + '/'

        // if (angular.isUndefined($scope.cache.get(datajson))) {

        sigma.parsers.json(apicall, {
                renderer: {
                    container: document.getElementById('sigma-container'),
                    type: 'canvas',


                },

                settings: {
                    maxNodeSize: 20,
                    minNodeSize: 4,
                    minEdgeSize: 1,
                    maxEdgeSize: 1,
                    minArrowSize: 25,
                    labelThreshold: 75,
                    defaultLabelSize: 25,
                    doubleClickEnabled: false,

                }
            },

            function (sigmaInstance) {

                sigmaInstance.graph.nodes().forEach(function (node, i, a) {

                    node.x = Math.cos(Math.PI * 2 * i / a.length);
                    node.y = Math.sin(Math.PI * 2 * i / a.length);

                });

                sigmaInstance.startForceAtlas2({
                    worker: true,
                    barnesHutOptimize: false,
                    scalingRatio: 2,
                    gravity: 1,
                    linLogMode: true,
                });


                if (sigmaInstance.graph.nodes().length > 75) {
                    setTimeout(function () {
                        $scope.cache.put(datajson, sigmaInstance.graph.nodes());
                        sigmaInstance.stopForceAtlas2();


                    }, 3000);

                } else {

                    setTimeout(function () {
                        $scope.cache.put(datajson, sigmaInstance.graph.nodes());


                    }, 1200);


                }
                sigmaInstance.graph.nodes().forEach(function (n) {
                    n.originalColor = n.color;
                });
                sigmaInstance.graph.edges().forEach(function (e) {
                    e.originalColor = e.color;
                });


                sigmaInstance.bind('clickNode', function (e) {

                    if (!$scope.wordcloud) {
                        $scope.Proyecto = [];

                        var idtocall = e.data.node.idproject;
                        var apiget = '/api/v1/data/project/?format=json&id=' + idtocall;
                        $http.get(apiget).then(function successCallback(response) {

                            $scope.Proyecto.push(response.data.results[0]);
                        });


                        debugger;


                    }
                    var nodeId = e.data.node.id,
                        toKeep = sigmaInstance.graph.neighbors(nodeId);
                    toKeep[nodeId] = e.data.node;
                    if (e.data.node.color != '#1954f2') {
                        if ($scope.wordcloud)
                            $scope.reloadinfoonclick(e.data.node.info);


                    }
                    sigmaInstance.graph.nodes().forEach(function (n) {
                        if (toKeep[n.id]) {
                            n.color = n.originalColor;
                            e.data.node.color = '#1954f2'
                        }
                        else {
                            n.color = 'rgba(198, 36, 63, 0.15)';

                        }
                    });

                    sigmaInstance.graph.edges().forEach(function (e) {

                        if (toKeep[e.source] && toKeep[e.target])
                            e.color = e.originalColor;
                        else {
                            e.color = 'rgba(198, 36, 63, 0.05)';

                        }
                    });

                    sigmaInstance.refresh();


                });
                sigmaInstance.bind('overNode', function (e) {

                    if ($scope.wordcloud)
                        $scope.reloadinfoonhover(e.data.node.info);


                });
                sigmaInstance.bind('doubleClickNode', function (e) {
                    debugger;
                    var community = e.data.node.label.split(' - ')[0];

                    sigmaInstance.graph.clear();
                    sigmaInstance.refresh();
                    $scope.communityObject(community)

                });


            }
        );


    };


    $scope.loadparallels = function () {

        document.getElementById('container').style.display = 'none'
        document.getElementById('sigma-container').style.display = 'none'
        document.getElementById('wordcloud').style.display = 'none'
        document.getElementById('projectid').style.display = 'none'
        document.getElementById('loader').style.display = ''
        document.getElementById('grid').style.display = 'none'


        document.getElementById('loadparallel').style.display = ''
        document.getElementById('choseparallel').style.display = ''
        $scope.parallelcoordinates("")

        $scope.comunidad = "";
        $scope.lessP = 0;
        $scope.moreP = 0;
        $scope.lessS = 0;
        $scope.moreS = 0;
        $scope.titulo = "";
        $scope.pais = "";


        function compare(a, b) {
            if (parseInt(a.communityId) < parseInt(b.communityId))
                return -1;
            if (parseInt(a.communityId) > parseInt(b.communityId))
                return 1;
            return 0;
        }

        $http.get('/api/v1/data/AllCommunity/').then(function (communityresponse) {

            if (communityresponse.data) {

                $scope.communities = communityresponse.data.results;
                $scope.communities.sort(compare);


            } else {
                $scope.communities = null;
            }
        });


    }


    $scope.parallelcoordinates = function (url) {

        debugger;
        document.getElementById('choseparallel').style.display = ""
        document.getElementById('parallel').innerHTML = ""
        document.getElementById('grid').style.display = ''


        var apiget = '/api/v1/data/GraphH2020/?limit=14837&offset=0' + url;
        $scope.paralleldata = []
        $http.get(apiget).then(function successCallback(response) {

            $scope.paralleldata.push(response.data.results);
            document.getElementById('loader').style.display = 'none'

            d3.json(JSON.stringify($scope.paralleldatada), function (data) {
                var datagraph = $scope.paralleldata
                var format = d3.time.format("%Y-%m-%d");
                var formatDate = d3.time.format("%Y")
                datagraph[0].forEach(function (d, i) {

                    if (d.startdate == null) {
                        delete datagraph[0][i];
                    }
                    d.startdate = formatDate(format.parse(d['startdate']));

                });


                var colorgen = d3.scale.ordinal()
                    .range(["#5DA5B3", "#D58323", "#DD6CA7", "#54AF52", "#8C92E8", "#E15E5A", "#725D82", "#776327", "#50AB84", "#954D56", "#AB9C27", "#517C3F", "#9D5130", "#357468", "#5E9ACF", "#C47DCB", "#7D9E33", "#DB7F85", "#BA89AD", "#4C6C86", "#B59248", "#D8597D", "#944F7E", "#D67D4B", "#8F86C2"]);


                var color = function (d) {
                    return colorgen(d.community);
                };


                debugger;

                var dimensions = {
                    "community":
                        {
                            orient: 'right',
                            type: 'number',
                            tickPadding: 0,
                            innerTickSize: 8,
                            ticks: 59

                        },

                    "presupuesto":
                        {
                            orient: 'right',
                            type: 'number',
                            tickPadding: 0,
                            innerTickSize: 8,
                            ticks: 10

                        },

                    "subvencion":
                        {
                            orient: 'right',
                            type: 'number',
                            tickPadding: 0,
                            innerTickSize: 8,
                            ticks: 10

                        },
                    "country":
                        {
                            orient: 'right',
                            type: 'string',
                            tickPadding: 0,
                            innerTickSize: 8,
                            ticks: function () {
                                var ticks = datagraph[0].map(function (obj) {
                                    return obj.country;
                                });
                                ticks = ticks.filter(function (v, i) {
                                    return (ticks.indexOf(v) == i);
                                });
                                return (ticks.length);
                            }

                        },
                    "startdate":
                        {
                            orient: 'right',
                            type: 'number',
                            tickPadding: 0,
                            innerTickSize: 8,
                        }

                };


                var parcoords = d3.parcoords()("#parallel")
                    .data(datagraph[0])
                    .hideAxis(["id", "idproject", "idnode", "tituloProyecto"])
                    .color(color)
                    .dimensions(dimensions)
                    .alpha(0.5)
                    .composite("darken")
                    .mode("queue")
                    .render()
                    .brushMode("1D-axes");  // enable brushing

                parcoords.svg.selectAll("text")
                    .style("font", "10px sans-serif");


                var grid = d3.divgrid();


                d3.select("#grid")
                    .datum(function () {

                        for (var i in datagraph[0].slice(0, 5)) {
                            delete datagraph[0][i]['idnode']
                            delete datagraph[0][i]['id']


                        }
                        return datagraph[0].slice(0, 5)
                    })
                    .call(grid)
                    .selectAll(".row")
                    .on({
                        "mouseover": function (d) {

                            parcoords.highlight([d])
                        },
                        "mouseout": parcoords.unhighlight
                    });
                // update data table on brush event
                parcoords.on("brush", function (d) {

                    d3.select("#grid")
                        .datum(function () {

                            for (var i in d.slice(0, 5)) {
                                delete d[i]['idnode']
                                delete d[i]['id']


                            }
                            return d.slice(0, 5)
                        })

                        .call(grid)
                        .selectAll(".row")
                        .on({
                            "mouseover": function (d) {
                                parcoords.highlight([d])
                            },
                            "mouseout": parcoords.unhighlight
                        });
                    //updateThumbnails(d);
                });

                // update data table on brush event

            });
        });
    }

    $scope.debug = function (a) {
        debugger;

    }

}
])
;


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

