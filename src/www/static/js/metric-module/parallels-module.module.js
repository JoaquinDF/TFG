'use strict';

angular.module('parallelsModule', []).controller('PARALLELS', ['$scope', '$http', '$routeParams', function ($scope, $http, $routeParams) {
    var ShowLoader = function () {
        document.getElementById('loader').style.display = ''
        document.getElementById('grid').style.display = 'none'

    }

    var HideLoader = function () {
        document.getElementById('loader').style.display = 'none'
        document.getElementById('grid').style.display = ''


    }
    $scope.loadparallels = function (data) {


        $scope.parallelcoordinates(data)


        $scope.comunidad = $routeParams.id == undefined ? "" : $routeParams.id;
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
        ShowLoader();

        debugger;
        document.getElementById('choseparallel').style.display = ""
        document.getElementById('parallel').innerHTML = ""
        document.getElementById('grid').style.display = ''


        var apiget = '/api/v1/data/GraphH2020/?limit=14837&offset=0' + url;
        $scope.paralleldata = []
        $http.get(apiget).then(function successCallback(response) {


            $scope.paralleldata.push(response.data.results);
            HideLoader();
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
                    "community": {
                        orient: 'right',
                        type: 'number',
                        tickPadding: 0,
                        innerTickSize: 8,
                        ticks: 59

                    },

                    "presupuesto": {
                        orient: 'right',
                        type: 'number',
                        tickPadding: 0,
                        innerTickSize: 8,
                        ticks: 10

                    },

                    "subvencion": {
                        orient: 'right',
                        type: 'number',
                        tickPadding: 0,
                        innerTickSize: 8,
                        ticks: 10

                    },
                    "country": {
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
                    "startdate": {
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

    if ($routeParams.id != undefined) {
        $scope.loadparallels('&community=' + $routeParams.id)
    } else {
        $scope.loadparallels("")


    }

}]);
