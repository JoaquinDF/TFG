'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.module('organizationList').component('organizationList', {

        templateUrl: '/static/templates/organization-list.template.html',
        controller: ['$http', function OrganizationListController($http, $scope) {
            var self = this;
            self.orgchange = 'EU'
            $http.get('/api/v1/data/organization/?limit=10&offset=0&ordering=nombre&nation=EU').then(function (responseorganizations) {

                self.organizations = responseorganizations.data.results;
                self.organizationsnext = responseorganizations.data.next;
                self.organizationsprev = responseorganizations.data.previous;
                self.countorganizations = Math.floor(((responseorganizations.data.count) / 10) + 1);
                self.currentpageorganizations = 1;
                self.pagecounterorganizations;

                self.nextorganization = function () {
                    if (self.organizationsnext) {
                        $http.get(self.organizationsnext).then(function (responseorganizations) {

                            if (responseorganizations.data) {

                                self.organizations = responseorganizations.data.results;
                                self.organizationsnext = responseorganizations.data.next;
                                self.organizationsprev = responseorganizations.data.previous;
                                self.currentpageorganizations += 1;
                                self.pagecounterorganizations = null;
                            }
                        });
                    }
                }
                self.prevorganization = function () {
                    if (self.currentpageorganizations > 1) {
                        $http.get(self.organizationsprev).then(function (responseorganizations) {
                            if (responseorganizations.data) {
                                self.organizations = responseorganizations.data.results;
                                self.organizationsnext = responseorganizations.data.next;
                                self.organizationsprev = responseorganizations.data.previous;
                                self.currentpageorganizations -= 1;
                                self.pagecounterorganizations = null;

                            }
                        });
                    }
                }


                self.onNationChanged = function (where) {
                    if (where) {
                        var togo = '/api/v1/data/organization/?limit=10&nation=' + where;

                        $http.get(togo).then(function (responseorganizations) {
                            if (responseorganizations.data) {
                                self.organizations = responseorganizations.data.results;
                                self.organizationsnext = responseorganizations.data.next;
                                self.organizationsprev = responseorganizations.data.previous;
                                self.countorganizations = Math.floor(((responseorganizations.data.count) / 10) + 1);
                                self.currentpageorganizations = 1;


                            }
                        });
                    }


                }

                self.onHoverMetrics = function (organization) {
                    if (!organization) return false;
                    var country = organization.direccion.pais;

                    var http = "/api/v1/data/RegionMetric/?region=" + country;

                    $http.get(http).then(function (responseorganizations) {
                        if (responseorganizations.data) {

                            var data = responseorganizations.data.results[0];

                            self.regionName = data.country;
                            self.numeroProyectosR = data.numeroProyectos;
                            self.porcentajesubvencionadoR = (parseFloat(data.porcentajesubvencionado)).toFixed(1);
                            self.numeroProyectosMedioR = (parseFloat(data.numeroProyectos) / parseFloat(data.numeroEmpresas)).toFixed(1);
                            self.numeroEmpresas = parseFloat(data.numeroEmpresas)

                            var http = "/api/v1/data/OrganizationMetric/?organization=" + organization.id;

                            $http.get(http).then(function (responseorganizations) {
                                if (responseorganizations.data) {

                                    var data = responseorganizations.data.results[0];

                                    self.porcentajesubvencionadoO = (parseFloat(data.porcentajeSubvencionado)).toFixed(1);
                                    self.numeroProyectosO = data.numeroProyectos;


                                    self.porcentajeRelativo = ((self.porcentajesubvencionadoO / self.porcentajesubvencionadoR)).toFixed(1);
                                    self.proyectosRelativo = (self.numeroProyectosO - self.numeroProyectosMedioR).toFixed(1)


                                }


                            });

                        }

                    });


                }


                self.changepage = function (page) {
                    if (!isNaN(page) && page && page <= self.countorganizations) {
                        self.currentpageorganizations = parseInt(page);
                        page *= 10;
                        page -= 10;
                        var http = "/api/v1/data/organization/?limit=10&offset=" + page + "&ordering=nombre";

                        $http.get(http).then(function (responseorganizations) {
                            if (responseorganizations.data) {

                                self.organizations = responseorganizations.data.results;
                                self.organizationsnext = responseorganizations.data.next;
                                self.organizationsprev = responseorganizations.data.previous;


                            }
                        });
                    }
                }

            });


        }]

    }
);
