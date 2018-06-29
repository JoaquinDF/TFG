'use strict';

/**
 * Controlador principal de las convocatorias
 * @namespace innhomeweb.Oranization-list
 */
// Register `projectList` component, along with its associated controller and template!
angular.module('organizationList').component('organizationList', {

        templateUrl: '/static/templates/organization-list.template.html',
        controller: ['$http', function OrganizationListController($http, $scope) {
            var self = this;
            self.orgchange = 'EU'
            self.orgfind = ""

            self.startingorganization = function () {
                /**
                 * Devuelve el listado inicial de organizaciones.
                 * @memberof innhomeweb.Oranization-list
                 * @method startingorganization
                 * @returns {Array}
                 */
                $http.get('/api/v1/data/organization/?limit=10&offset=0&ordering=nombre&nation=EU').then(function (responseorganizations) {

                    self.organizations = responseorganizations.data.results;
                    self.organizationsnext = responseorganizations.data.next;
                    self.organizationsprev = responseorganizations.data.previous;
                    self.countorganizations = Math.floor(((responseorganizations.data.count) / 10) + 1);
                    self.currentpageorganizations = 1;
                    self.pagecounterorganizations;
                });

            }


            self.nextorganization = function () {
                /**
                 * Devuelve el listado siguiente de organizaciones.
                 * @memberof innhomeweb.Oranization-list
                 * @method nextorganization
                 *@returns {array}
                 */
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
                /**
                 * Devuelve el listado anterior de organizaciones.
                 * @memberof innhomeweb.Oranization-list
                 * @method prevorganization
                 *@returns {array}
                 */
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

            self.lastorganization = function () {
                /**
                 * Devuelve el listado con las últimas organizaciones.
                 * @memberof innhomeweb.Oranization-list
                 * @method lastorganization
                 *@returns {array}
                 */
                var page = self.countorganizations;
                page *= 10;
                page -= 10;
                var apitogo = "/api/v1/data/Organization/?limit=10&offset=" + page + "&ordering=nombre";
                $http.get(apitogo).then(function (responseorgs) {

                    self.organizations = responseorgs.data.results;
                    self.organizationsnext = responseorgs.data.next;
                    self.organizationsprev = responseorgs.data.previous;
                    self.currentpage = self.countorganizations;
                });
            }


            self.onNationChanged = function (where) {
                /**
                 * Cambia de nación dentro del listado de organizaciones.
                 * @memberof innhomeweb.Oranization-list
                 * @method onNationChanged
                 *  @param {string} where Recibe la nación a la que se quiere cambiar
                 *@returns {array}
                 */

                debugger;
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
                /**
                 * Carga las métricas de la organización determinada
                 * @memberof innhomeweb.Oranization-list
                 * @method onHoverMetrics
                 * @param {string} organization Carga las métricas de la organización
                 *@returns {array}
                 */

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
                /**
                 * Cambia de página dentro del listado de organizaciones.
                 * @memberof innhomeweb.Oranization-list
                 * @method changepage
                 * @param {string} page Recibe la página a la que se quiere cambiar
                 * @returns {array}
                 */

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

            self.findOrganization = function (toFind) {
                /**
                 * Devuelve el listado con las organizaciones buscadas.
                 * @memberof innhomeweb.Oranization-list
                 * @method findOrganization
                 * @param {string} toFind Recibe una cadena y busca las organizaciones que contengan esa cadena
                 * @returns {array}
                 */
                if ((toFind != "") && toFind) {
                    self.Organizationfind = toFind
                    var http = "/api/v1/data/organization/?limit=10&offset=0&ordering=nombre&name=" + toFind;

                    $http.get(http).then(function (responseorganizations) {
                        if (responseorganizations.data) {

                            self.organizations = responseorganizations.data.results;
                            self.organizationsnext = responseorganizations.data.next;
                            self.organizationsprev = responseorganizations.data.previous;
                            self.countorganizations = Math.floor(((responseorganizations.data.count) / 10) + 1);
                            self.currentpageorganizations = 1;

                        }
                    });
                } else {

                    self.startingorganization()


                }

            }

            self.saveedit = function () {
                /**
                 * Postea el cambio contra la API
                 * @memberof innhomeweb.Oranization-list
                 * @method saveedit
                 */

                var keys = Object.keys(self.EditOrganization);
                var tosave = {}


                for (var key in keys) {
                    tosave[keys[key]] = $('#' + keys[key]).val()
                }
                tosave['keys'] = keys.join()

                $http.put('/api/v1/data/organization/' + self.EditOrganization['id'] + '/', tosave).then(function successCallback(response) {

                    self.findOrganization(self.EditOrganization)

                }, function errorCallback(response) {

                    debugger;
                });


            }


            self.editOrganization = function (idtoEdit) {
                /**
                 * Abre el modal para proceder con el edit.
                 * @memberof innhomeweb.Oranization-list
                 * @method editOrganization
                 * @param {string} idtoEdit Indica el id del objecto que se va a editar
                 */
                self.EditOrganization = [];
                var http = "/api/v1/data/organization/?id=" + idtoEdit;
                $http.get(http).then(function (responseprojects) {
                    if (responseprojects.data) {

                        self.EditOrganization = responseprojects.data.results[0];
                        $('#editOrganization').modal('show')

                    }
                });


            }

            self.startingorganization()

        }]

    }
);
