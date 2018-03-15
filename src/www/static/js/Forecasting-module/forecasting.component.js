'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.module('forecastingModule').component('forecastingModule', {

        templateUrl: '/static/templates/forecasting.template.html',
        controller: ['$http', function forecastingController($http, $scope) {

            var self = this;
            self.search = "";

            self.keydown = function (keyEvent) {
                console.log('keydown -' + keyEvent);
                if (keyEvent.key == 'Enter') {

                    debugger;

                    self.data = {
                        entry: this.search
                    };

                    document.getElementById('loader').style.display = ''


                    $http.post('/api/v1/data/CommunityEstimation/', self.data).then(function successCallback(response) {
                        document.getElementById('entry').style.height = "100px"
                        document.getElementById('loader').style.display = 'none'
                        self.estimation = response.data;
                        self.loadgraph(self.estimation)
                        debugger;

                    }, function errorCallback(response) {


                    });

                }
            };


            self.drawWordCloud = function (text, svglocation) {


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

                d3.layout.cloud().stop();
            };


            self.reloadinfoonclick = function (info) {


                document.getElementById("nodeinfo").innerHTML = "";

                var arraydata = info.split(",");
                self.drawWordCloud(arraydata, '#nodeinfo')


            };

            self.reloadinfoonhover = function (info) {
                document.getElementById("nodeinfohover").innerHTML = "";

                var arraydata = info.split(",");
                self.drawWordCloud(arraydata, '#nodeinfohover')


            };

            hexToRGB = function (hex) {
                var r = hex >> 16;
                var g = hex >> 8 & 0xFF;
                var b = hex & 0xFF;
                return [r, g, b];
            }
            self.loadgraph = function (datajson) {
                document.getElementById('sigma-container').style.display = "block";
                document.getElementById('sigma-container').innerHTML = ""


                var apicall = '/api/v1/test-files/' + 'h2020'


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
                            color = [3]
                            color = hexToRGB(node.color)

                            //TODO Hacer que cada nodo ajuste la intensidad de su color a la calidad de los datos.

                        });

                        sigmaInstance.startForceAtlas2({
                            worker: true,
                            barnesHutOptimize: false,
                            scalingRatio: 2,
                            gravity: 1,
                            linLogMode: true,
                        });


                        setTimeout(function () {
                            sigmaInstance.stopForceAtlas2();


                        }, 3000);


                        sigmaInstance.bind('clickNode', function (e) {


                            self.reloadinfoonclick(e.data.node.info);


                        });


                        sigmaInstance.bind('overNode', function (e) {

                            self.reloadinfoonhover(e.data.node.info);


                        });
                        sigmaInstance.refresh();

                    });


            };


        }]

    }
);
