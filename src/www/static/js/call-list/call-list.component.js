'use strict';

// Register `countList` component, along with its associated controller and template!
angular.module('callList').component('callList', {

        templateUrl: '/static/templates/call-list.template.html',
        controller: ['$http', function CallsListController($http, $scope) {
            var self = this;
            self.callfind = ""


            self.startingcall = function () {

                $http.get('/api/v1/data/call/?limit=10&offset=10&ordering=tituloConvocatoria').then(function (responsecalls) {

                    self.calls = responsecalls.data.results;
                    self.callsnext = responsecalls.data.next;
                    self.callsprev = responsecalls.data.previous;
                    self.countcalls = Math.floor(((responsecalls.data.count) / 10) + 1);
                    self.currentpagecalls = 1;
                });
            }
            self.nextcall = function () {
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
