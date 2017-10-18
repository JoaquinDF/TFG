'use strict';

// Register `countList` component, along with its associated controller and template!
angular.module('metricModule').component('metricModule', {

        templateUrl: '/static/templates/metric-module.template.html',
    controller: ['$http', '$rootScope', function CallsListController($http, $rootScope) {
            var self = this;
            self.porcentajesubvencionado = 0;
            self.calculateMetrics = function (proy) {
                self.porcentajesubvencionado += (parseFloat(proy.subvencion) / parseFloat(proy.presupuestoAceptado) )
                $rootScope.averagesubvencionado = parseInt((self.porcentajesubvencionado / self.Proyecto.length) * 100);
            }


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

                        });
                        var apiget = '/api/v1/data/projectorganization/?format=json&organization=' + organizationid;

                        $http.get(apiget).then(function successCallback(response) {
                            var projectidarray = response.data.results;

                            self.Proyecto = [];

                            projectidarray.forEach(function (id) {


                                var apiget = '/api/v1/data/project/?format=json&id=' + id.proyecto;
                                $http.get(apiget).then(function successCallback(response) {

                                    self.Proyecto.push(response.data.results[0]);
                                    self.calculateMetrics(response.data.results[0]);
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


        }]

    }
);
