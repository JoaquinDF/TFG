'use strict';
angular.module('communityModule', []).controller('COMMUNITY', ['$scope', '$http', '$routeParams', function ($scope, $http, $routeParams) {


    $scope.nodeinfo = [];

    $scope.tofind = function (data) {

        for (var instance in sigma.instances()) {
            console.log(instance);
            var sigmainstance = sigma.instances()[instance]

            if (!data == "") {
                if (!isNaN(data)) { //es un numero
                    sigmainstance.graph.nodes().forEach(function (n) {
                        if (parseFloat(data) != n.id) {
                            n.color = 'rgb(211,211,211,0.3)'

                        } else {
                            n.color = n.originalColor
                        }
                    });
                } else {

                    sigmainstance.graph.nodes().forEach(function (n) {
                        if (n.info.indexOf(data) == -1) {
                            n.color = 'rgb(211,211,211,0.3)'

                        } else {
                            n.color = n.originalColor
                        }
                    });


                }
                sigmainstance.graph.edges().forEach(function (e) {


                    e.color = 'rgba(198, 36, 63, 0.05)';


                });

            } else {

                sigmainstance.graph.nodes().forEach(function (n) {
                    n.color = n.originalColor


                });
                sigmainstance.graph.edges().forEach(function (e) {


                    e.color = e.originalColor;


                });


            }
            sigmainstance.refresh()
        }

    }

    $scope.showwordcloud = function (value) {
        if (value) {
            document.getElementById('nodeinfohover').style.display = ''

            document.getElementById('projectid').style.display = "none"

            $scope.wordcloud = value

        } else {
            document.getElementById('nodeinfohover').style.display = "none"
            document.getElementById('projectid').style.display = ""

            $scope.wordcloud = value


        }

    }

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
            d3.select(svg_location).select("svg").remove();
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
        document.getElementById('sigma-container').style.display = "block";
        document.getElementById('sigma-container').innerHTML = ""

        var a = parseInt(datajson)
        if (isNaN(a)) {
            $scope.showwordcloud(true)
        } else {
            $scope.showwordcloud(false)


        }

        ShowLoader()
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
                HideLoader()


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
                        sigmaInstance.stopForceAtlas2();
                        document.getElementById('finder').style.display = ''


                    }, 3000);

                } else {

                    setTimeout(function () {

                        sigmaInstance.stopForceAtlas2();
                        document.getElementById('finder').style.display = ''


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
                sigmaInstance.bind('clickStage', function (e) {

                    sigmaInstance.graph.nodes().forEach(function (n) {
                        n.color = n.originalColor


                    });
                    sigmaInstance.graph.edges().forEach(function (e) {
                        e.color = e.originalColor


                    });

                });


            }
        );


    };

    $scope.onURLclick = function (url1, url2) {
        var url = "/www/#!" + url1 + '/' + url2

        $window.location.href = url
    }
    var ShowLoader = function () {
        document.getElementById('finder').style.display = 'none'

        document.getElementById('loader').style.display = ''

    }

    var HideLoader = function () {
        document.getElementById('loader').style.display = 'none'

    }

    $scope.communityObject($routeParams.group)

}])
;