'use strict';

// Register `countList` component, along with its associated controller and template!


/**
 * Controlador principal de las convocatorias
 * @namespace innhomeweb.Call-list
 */


angular.module('callList').component('callList', {

        templateUrl: '/static/templates/call-list.template.html',
        controller: ['$http', function CallsListController($http, $scope) {
            var self = this;
            self.callfind = ""



            self.startingcall = function () {
                /**
                 * Devuelve el listado inicial de convocatorias.
                 * @memberof innhomeweb.Call-list
                 * @method startingcall
                 * @returns {Array}
                 */


                $http.get('/api/v1/data/call/?limit=10&offset=10&ordering=tituloConvocatoria').then(function (responsecalls) {

                    self.calls = responsecalls.data.results;
                    self.callsnext = responsecalls.data.next;
                    self.callsprev = responsecalls.data.previous;
                    self.countcalls = Math.floor(((responsecalls.data.count) / 10) + 1);
                    self.currentpagecalls = 1;
                });
            }
            self.nextcall = function () {
                /**
                 * Devuelve el listado siguiente de convocatorias.
                 * @memberof innhomeweb.Call-list
                 * @method nextcall
                 *@returns {array}
                 */

                if (self.callsnext) {
                    $http.get(self.callsnext).then(function (responsecalls) {

                        if (responsecalls.data) {

                            self.calls = responsecalls.data.results;

                            self.callsnext = responsecalls.data.next;
                            self.callsprev = responsecalls.data.previous;
                            self.currentpagecalls += 1;
                        }
                    });
                }
            }
            self.prevcall = function () {

                /**
                 * Devuelve el listado anterior de convocatorias.
                 * @memberof innhomeweb.Call-list
                 * @method prevcall
                 *@returns {array}
                 */

                if (self.currentpagecalls > 1) {
                    $http.get(self.callsprev).then(function (responsecalls) {
                        if (responsecalls.data) {
                            self.calls = responsecalls.data.results;
                            self.callsnext = responsecalls.data.next;
                            self.callsprev = responsecalls.data.previous;
                            self.currentpagecalls -= 1;
                            self.pagecountercalls = null;

                        }
                    });
                }
            }

            self.lastcall = function () {


                /**
                 * Devuelve el listado con las últimas convocatorias.
                 * @memberof innhomeweb.Call-list
                 * @method lastcall
                 *@returns {array}
                 */

                var page = self.countcalls;
                page *= 10;
                page -= 10;
                var apitogo = "/api/v1/data/call/?limit=10&offset=" + page + "&ordering=tituloConvocatoria";
                $http.get(apitogo).then(function (responsecalls) {

                    self.calls = responsecalls.data.results;
                    self.callsnext = responsecalls.data.next;
                    self.callsprev = responsecalls.data.previous;
                    self.currentpage = self.countcalls;
                });
            }
            self.changepage = function (page) {

                /**
                 * Cambia de página dentro del listado de convocatorias.
                 * @memberof innhomeweb.Call-list
                 * @method changepage
                 *  @param {string} page Recibe la página a la que se quiere cambiar

                 *@returns {array}
                 */


                if (!isNaN(page) && page && page <= self.countcalls) {
                    self.currentpagecalls = parseInt(page);
                    page *= 10;
                    page -= 10;
                    var http = "/api/v1/data/call/?limit=10&offset=" + page + "&ordering=tituloConvocatoria";

                    $http.get(http).then(function (responsecalls) {
                        if (responsecalls.data) {

                            self.calls = responsecalls.data.results;
                            self.callsnext = responsecalls.data.next;
                            self.callsprev = responsecalls.data.previous;


                        }
                    });
                }
            }

            self.findCall = function (toFind) {


                /**
                 * Devuelve el listado con las convocatorias buscadas.
                 * @memberof innhomeweb.Call-list
                 * @method findCall
                 *@param {string} toFind Recibe una cadena y busca las convocatorias que contengan esa cadena
                 *@returns {array}
                 */


                if ((toFind != "") && toFind) {
                    self.callfind = toFind
                    var http = "/api/v1/data/call/?limit=10&offset=0&ordering=tituloConvocatoria&name=" + toFind;

                    $http.get(http).then(function (responsecalls) {
                        if (responsecalls.data) {

                            self.calls = responsecalls.data.results;
                            self.callsnext = responsecalls.data.next;
                            self.callsprev = responsecalls.data.previous;
                            self.countcalls = Math.floor(((responsecalls.data.count) / 10) + 1);
                            self.currentpagecalls = 1;
                        }
                    });
                } else {

                    self.startingcall()


                }

            }

            self.saveedit = function () {


                /**
                 * Postea el cambio contra la API
                 * @memberof innhomeweb.Call-list
                 * @method saveedit
                 */


                var keys = Object.keys(self.EditcallObject);
                var tosave = {}


                for (var key in keys) {
                    tosave[keys[key]] = $('#' + keys[key]).val()
                }
                tosave['keys'] = keys.join()

                $http.put('/api/v1/data/call/' + self.EditcallObject['id'] + '/', tosave).then(function successCallback(response) {

                    self.findCall(self.callfind)

                }, function errorCallback(response) {

                    debugger;
                });


            }


            self.editCall = function (idtoEdit) {

                /**
                 * Abre el modal para proceder con el edit.
                 * @memberof innhomeweb.Call-list
                 * @method editCall
                 *@param {string} idtoEdit Indica el id del objecto que se va a editar

                 */




                self.EditcallObject = [];
                var http = "/api/v1/data/call/?id=" + idtoEdit;
                $http.get(http).then(function (responseprojects) {
                    if (responseprojects.data) {

                        self.EditcallObject = responseprojects.data.results[0];
                        $('#editCall').modal('show')

                    }
                });


            }
            self.startingcall();


        }]

    }
)
;
