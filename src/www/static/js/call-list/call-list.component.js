'use strict';

// Register `countList` component, along with its associated controller and template!
angular.module('callList').component('callList', {

        templateUrl: '/static/templates/call-list.template.html',
        controller: ['$http', function CallsListController($http, $scope) {
            var self = this;
            $http.get('/api/v1/data/call/?limit=10&offset=10&ordering=tituloConvocatoria').then(function (responsecalls) {

                self.calls = responsecalls.data.results;
                self.callsnext = responsecalls.data.next;
                self.callsprev = responsecalls.data.previous;
                debugger;
                self.countcalls = Math.floor(((responsecalls.data.count) / 10)+1);
                self.currentpagecalls = 1;
                self.pagecountercalls;

                self.nextcall = function () {
                    if (self.callsnext) {
                        $http.get(self.callsnext).then(function (responsecalls) {

                            if (responsecalls.data) {

                                self.calls = responsecalls.data.results;

                                self.callsnext = responsecalls.data.next;
                                self.callsprev = responsecalls.data.previous;
                                self.currentpagecalls += 1;
                                self.pagecountercalls=null;
                            }
                        });
                    }
                }
                self.prevcall = function () {
                    if (self.currentpagecalls > 0) {
                        $http.get(self.callsprev).then(function (responsecalls) {
                            if (responsecalls.data) {
                                self.calls = responsecalls.data.results;
                                self.callsnext = responsecalls.data.next;
                                self.callsprev = responsecalls.data.previous;
                                self.currentpagecalls -= 1;
                                self.pagecountercalls=null;

                            }
                        });
                    }
                }


                self.changepage = function (page) {
                    if (!isNaN(page) && page && page <= self.countcalls) {
                          self.currentpagecalls = parseInt(page);
                        page *= 10;
                        page-=10;
                        var http = "/api/v1/data/call/?limit=10&offset="+page + "&ordering=tituloConvocatoria";

                        $http.get(http).then(function (responsecalls) {
                            if (responsecalls.data) {

                                self.calls = responsecalls.data.results;
                                self.callsnext = responsecalls.data.next;
                                self.callsprev = responsecalls.data.previous;


                            }
                        });
                    }
                }

            });


        }]

    }
);
