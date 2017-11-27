'use strict';

// Register `countList` component, along with its associated controller and template!
angular.module('metricModule').component('metricModule', {

        templateUrl: '/static/templates/metric-module.template.html',
    controller: ['$http', function CallsListController($http) {
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
                            debugger;
                            var http = "/api/v1/data/RegionMetric/?region=" + self.Orgs[0].direccion.pais;

                            $http.get(http).then(function (responseorganizations) {
                                if (responseorganizations.data) {

                                    var data = responseorganizations.data.results[0];

                                    self.regionName = data.country;
                                    self.numeroProyectosR = data.numeroProyectos;
                                    self.porcentajesubvencionadoR = (parseFloat(data.porcentajesubvencionado)).toFixed(1);
                                    debugger;
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
                                self.loadpieporcentaje();


                                self.porcentajeRelativo = ((self.porcentajesubvencionadoO / self.porcentajesubvencionadoR) * 100).toFixed(1);
                                self.proyectosRelativo = (self.numeroProyectosO - self.numeroProyectosMedioR).toFixed(1)
                                debugger;

                            }


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

        self.loadpieporcentaje = function () {
            var labelsubv = 'Presupuesto Subvencionado - %';
            var labelsinsubv = 'Presupuesto sin Subvencionar - %';
            self.labelspie = [labelsubv, labelsinsubv];

            self.datapie = [self.porcentajesubvencionadoO, (100 - self.porcentajesubvencionadoO)];
            self.optionspie = {
                tooltips: {bodyFontSize: 20, titleFontSize: 15, fontColor: 'rgb(255, 99, 132)'},
                responsive: true,
                maintainAspectRatio: true
            };
            var labelsubvbar = 'Media Empresarial subvencion';
            var labelsinsubvbar = 'Medio Regional subvencion';
            self.seriesbar = [labelsubvbar, labelsinsubvbar];
            debugger;
            self.databar = [[self.porcentajesubvencionadoO], [self.porcentajesubvencionadoR]];
            self.optionsbar = {
                tooltips: {bodyFontSize: 20, titleFontSize: 15, fontColor: 'rgb(255, 99, 132)'},
                responsive: true,
                maintainAspectRatio: true
            };


            var canvas = document.getElementById("pie");
            self.datapie = [self.porcentajesubvencionadoO, (100 - self.porcentajesubvencionadoO)];
            debugger;
            canvas.config.data = self.datapie;
            debugger;

            canvas.update();
            debugger;


            var canvas = document.getElementById("bar");
            self.databar = [[self.porcentajesubvencionadoO], [self.porcentajesubvencionadoR]];
            debugger;
            canvas.config.data = self.databar;
            debugger;

            canvas.update();
            debugger;

        }
        }]

    }
);