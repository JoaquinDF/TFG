'use strict';

// Register `countList` component, along with its associated controller and template!
angular.module('searchList').component('searchList', {

        templateUrl: '/static/templates/search-list.template.html',
        controller: ['$http', function CallsListController($http, $scope) {
            var self = this;
            var x = document.URL;

            var projectid, organizationid, callid;
            debugger;
            var regex = new RegExp('\/(p|o|c|np|no|nc)[0-9a-zA-Z]*');

            var tipo = regex.exec(x);
            if (tipo != null) {
                debugger;
                switch (tipo[1]) {

                    case 'p':

                        projectid = (tipo[0].split('/p'))[1];

                        var apiget = '/api/v1/data/project/?format=json&id=' + projectid;
                        $http.get(apiget).then(function successCallback(response) {
                            self.Proyecto = response.data.results;
                            self.Proyectosize = self.Proyecto.length;

                        }, function errorCallback(response) {
                        });


                        var apiget = '/api/v1/data/projectcall/?format=json&project=' + projectid;
                        $http.get(apiget).then(function successCallback(response) {
                            var callidarray = response.data.results;
                            callidarray.forEach(function (parameters) {
                                var id = parameters.convocatoria;
                                var apiget = '/api/v1/data/call/?format=json&id=' + id;
                                $http.get(apiget).then(function successCallback(response) {
                                    self.Calls = [];
                                    self.Calls.push(response.data.results[0])
                                });

                            });
                        });
                        var apiget = '/api/v1/data/projectorganization/?format=json&project=' + projectid;
                        $http.get(apiget).then(function successCallback(response) {
                            self.Orgs = [];
                            var orgidarray = response.data.results;
                            orgidarray.forEach(function (id) {

                                var apiget = '/api/v1/data/organization/?format=json&id=' + id.organizacion;
                                $http.get(apiget).then(function successCallback(response) {
                                    self.Orgs.push(response.data.results[0])
                                });

                            });
                        });

                        break;


                    case 'np':
                        callid = (tipo[0].split('/np'))[1];
                        var apiget = '/api/v1/data/project/?format=json&name=' + callid;
                        self.Proyecto = [];
                        $http.get(apiget).then(function successCallback(response) {
                            self.Proyecto = (response.data.results)
                        });

                        break;

                    case 'c':
                        callid = (tipo[0].split('/c'))[1];
                        var apiget = '/api/v1/data/call/?format=json&id=' + callid;

                        $http.get(apiget).then(function successCallback(response) {
                            self.Calls = [];
                            self.Calls = response.data.results;

                        });
                        var apiget = '/api/v1/data/projectcall/?format=json&call=' + callid;

                        $http.get(apiget).then(function successCallback(response) {
                            var projectidarray = response.data.results;
                            self.Proyecto = [];

                            projectidarray.forEach(function (id) {


                                var apiget = '/api/v1/data/project/?format=json&id=' + id.proyecto;
                                $http.get(apiget).then(function successCallback(response) {

                                    self.Proyecto.push(response.data.results[0])
                                    self.Proyectosize = self.Proyecto.length;

                                });


                            });


                        });


                        break;

                    case 'nc':
                        callid = (tipo[0].split('/nc'))[1];
                        var apiget = '/api/v1/data/call/?format=json&name=' + callid;
                        self.Calls;
                        $http.get(apiget).then(function successCallback(response) {
                            self.Calls = (response.data.results)
                        });

                        break;


                    case 'o':
                        organizationid = (tipo[0].split('/o'))[1];
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

                                    self.Proyecto.push(response.data.results[0])
                                    self.Proyectosize = self.Proyecto.length;

                                });


                            });


                        });

                        break;

                    case 'no':
                        callid = (tipo[0].split('/no'))[1];
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
