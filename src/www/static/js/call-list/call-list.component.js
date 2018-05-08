'use strict';

// Register `countList` component, along with its associated controller and template!
/**
 * @namespace innhomeweb
 *
 */

/**
 * @class innhomeweb.callList
 * @memberOf innhomeweb
 */

/**
 * @name startingcall
 * @function
 * @memberOf innhomeweb.callList.CallsListController
 * @returns {Array}  Devuelve el listado inicial de convocatorias.
 */


angular.module('callList').component('callList', {

        templateUrl: '/static/templates/call-list.template.html',
        controller: ['$http', function CallsListController($http, $scope) {
            var self = this;
            self.callfind = ""


            /**
             * A test module foo
             * @version 1.0
             * @exports mystuff/foo
             * @namespace foo
             */
            self.startingcall = function () {
                /**
                 * A method in first level, just for test
                 * @memberof foo
                 * @method testFirstLvl
                 */
                /**
                 * @name startingcall
                 * @function
                 * @memberOf innhomeweb.callList.CallsListController
                 * @returns {Array}  Devuelve el listado inicial de convocatorias.
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
                 * @name nextcall
                 * @function
                 * @memberOf innhomeweb.callList.CallsListController
                 *@returns {array} Devuelve el listado siguiente de convocatorias.
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
                 * @name prevcall
                 * @function
                 * @memberOf innhomeweb.callList.CallsListController
                 *@returns {array} Devuelve el listado anterior de convocatorias.
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
                 * @name lastcall
                 * @function
                 * @memberOf innhomeweb.callList.CallsListController
                 *@returns {array} Devuelve el listado con las últimas convocatorias.
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
                 * @name changepage
                 * @function
                 * @memberOf innhomeweb.callList.CallsListController
                 *@param {string} Recibe la página a la que se quiere cambiar
                 *@returns {array} Cambia de página.
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
                 * @name findCall
                 * @function
                 * @memberOf innhomeweb.callList.CallsListController
                 *@param {string} Recibe una cadena y busca las convocatorias que contengan esa cadena
                 *@returns {array} Devuelve el listado con las convocatorias.
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
                 * @name saveedit
                 * @function
                 * @memberOf innhomeweb.callList.CallsListController
                 * @description Postea el cambio contra la API

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
                 * @name editCall

                 * @function
                 * @memberOf innhomeweb.callList.CallsListController
                 * @description Abre el modal para proceder con el edit
                 * @param  Indica el id del objecto que se va a editar
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
