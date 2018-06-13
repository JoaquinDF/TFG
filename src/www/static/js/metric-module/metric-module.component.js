'use strict';

// Register `countList` component, along with its associated controller and template!
angular.module('metricModule').component('metricModule', {

        templateUrl: '/static/templates/metric-module.template.html',
        controller: ['$http', '$routeParams', function CallsListController($http, $routeParams) {
            var self = this;


            var x = document.URL;
            self.options = [{
                'value': 'metric',
                'name': 'Id Organization',

            },
                {
                    'value': 'metricn',
                    'name': 'Name organization',
                }];
            var projectid, organizationid, callid;
            var regex = new RegExp('\/metric(n)?[0-9a-zA-Z]+');

            var tipo = regex.exec(x);
            if (tipo != null) {
                switch (tipo[1]) {

                    default:
                        organizationid = (tipo[0].split('/metric'))[1];
                        var apiget = '/api/v1/data/organization/?format=json&id=' + organizationid;

                        $http.get(apiget).then(function successCallback(response) {
                            self.Orgs = [];
                            self.Orgs = response.data.results;
                            var http = "/api/v1/data/RegionMetric/?region=" + self.Orgs[0].direccion.pais;

                            $http.get(http).then(function (responseorganizations) {
                                if (responseorganizations.data) {

                                    var data = responseorganizations.data.results[0];

                                    self.regionName = data.country;
                                    self.numeroProyectosR = data.numeroProyectos;
                                    self.porcentajesubvencionadoR = (parseFloat(data.porcentajesubvencionado)).toFixed(1);
                                    self.numeroProyectosMedioR = (parseFloat(data.numeroProyectos) / parseFloat(data.numeroEmpresas)).toFixed(1);
                                    self.numeroEmpresas = parseFloat(data.numeroEmpresas)


                                }
                            });
                        });
                        var apiget = '/api/v1/data/projectorganization/?format=json&organization=' + organizationid;

                        $http.get(apiget).then(function successCallback(response) {
                            var projectidarray = response.data.results;

                            self.Proyecto = [];

                            projectidarray.forEach(function (id) {


                                var apiget = '/api/v1/data/project/?format=json&id=' + id.proyecto;
                                $http.get(apiget).then(function successCallback(response) {

                                    self.Proyecto.push(response.data.results[0]);
                                });


                            });


                        });


                        var http = "/api/v1/data/OrganizationMetric/?organization=" + organizationid;

                        $http.get(http).then(function (responseorganizations) {
                            if (responseorganizations.data) {

                                var data = responseorganizations.data.results[0];

                                self.porcentajesubvencionadoO = (parseFloat(data.porcentajeSubvencionado)).toFixed(1);
                                self.numeroProyectosO = data.numeroProyectos;


                                self.porcentajeRelativo = ((self.porcentajesubvencionadoO / self.porcentajesubvencionadoR) * 100).toFixed(1);
                                self.proyectosRelativo = (self.numeroProyectosO - self.numeroProyectosMedioR).toFixed(1)

                            }


                        });


                        var http = '/api/v1/data/organization/?format=json&id=' + organizationid;

                        $http.get(apiget).then(function successCallback(response) {
                            self.OrgsRelated = [];
                            self.OrgsRelated = response.data.results;

                        });
                        var apiget = '/api/v1/data/projectorganization/?format=json&organization=' + organizationid;

                        $http.get(apiget).then(function successCallback(response) {
                            var projectidarray = response.data.results;

                            self.PRelacionados = [];

                            projectidarray.forEach(function (id) {


                                var apiget = '/api/v1/data/project/?format=json&id=' + id.proyecto;
                                $http.get(apiget).then(function successCallback(response) {

                                    self.PRelacionados.push(response.data.results[0])

                                });


                            });


                        });


                        break;

                    case 'n':
                        callid = (tipo[0].split('/metricn'))[1];
                        var apiget = '/api/v1/data/organization/?format=json&name=' + callid;
                        self.Orgs;
                        $http.get(apiget).then(function successCallback(response) {
                            self.Orgs = (response.data.results)
                        });

                        break;

                }


            }


            self.toShow = function () {
                var a = $routeParams.id;
                if (a == null) {
                    return false
                } else {
                    return true
                }

            }


            self.loadcharts = function () {


                self.loadpie();
                self.loadbar()
                self.loadpolar()

            }

            self.loadpie = function () {
                var labelsubv = 'Presupuesto Subvencionado - %';
                var labelsinsubv = 'Presupuesto sin Subvencionar - %';
                self.labelspie = [labelsubv, labelsinsubv];
                self.datapie = [self.porcentajesubvencionadoO, ((100 - self.porcentajesubvencionadoO)).toFixed(1)];
            }
            self.loadbar = function () {
                var labelsubvbar = 'Subvencion Media en la empresa';
                var labelsinsubvbar = 'Subvencion Media del país';
                self.seriesbar = [labelsubvbar, labelsinsubvbar];
                self.databar = [[self.porcentajesubvencionadoO], [self.porcentajesubvencionadoR]];
            }


            self.loadpolar = function () {
                var country = self.regionName
                if (country) {

                    var setobject = {
                        "region": country
                    }

                    var apiget = '/api/v1/data/SectorMetric/'
                    $http.post(apiget, setobject).then(function successCallback(response) {
                        if (response.data) {


                            self.datapolar = []
                            var diff0 = 0
                            var sum = Object.values(response.data).reduce(function (pv, cv) {
                                return pv + cv;
                            }, 0);

                            Object.values(response.data).forEach(function (number) {

                                var a = (number / sum).toFixed(1)
                                if (a > 0.0) {
                                    diff0 += 1;
                                }
                                self.datapolar.push(a)
                            });


                            self.labelspolar = Object.keys(response.data)


                        }

                    });


                }


            }
        }]

    }
);
