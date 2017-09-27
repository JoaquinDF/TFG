'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.module('transformModule').component('transformModule', {

        templateUrl: '/static/templates/transform-module.template.html',
        controller: ['$http', '$timeout', function adminController($http, $timeout) {
            var self = this;
            self.MapperOptions = {};
            $http.get('/api/v1/transform/').then(function successCallback(response) {

                if (response.data) {

                    self.transforms = response.data


                } else {

                }

            }, function errorCallback(response) {
                //Error en la recogida de datos.
            });


            self.LaunchMapping = function () {

                var apiurl = self.selectedtransform;
                apiurl = apiurl.replace('mapper', 'mapping');
                debugger;

                var emptyjsontopost = {};

                $http.post(apiurl, emptyjsontopost).then(function successCallback(response) {

                    self.warning = 'CORRECT';
                }, function errorCallback(response) {
                    self.warning = 'ERROR'

                });

            }

            self.LoadMapper = function () {

                var apiurl = self.selectedtransform;
                debugger;


                $http.post(apiurl, self.MapperOptions).then(function successCallback(response) {

                    self.getMapperList();
                    self.warning = 'CORRECT';
                }, function errorCallback(response) {
                    self.warning = 'ERROR'

                });

            }
            self.setWarningSch = function () {
                $timeout(function () {
                    self.warning = null;
                }, 750);


            }
            self.deletekey = function (id) {

                var object = {id: id};
                var apiurl = self.selectedtransform;
                apiurl = apiurl.replace('transform/', 'transform/delete')
                debugger;


                $http.post(apiurl, object).then(function successCallback(response) {

                    self.getMapperList();

                }), function errorCallback(response) {
                    self.warning = 'ERROR'

                }
            }

            self.getMapperOptions = function () {
                if (self.selectedtransform && self.selectedtransform.indexOf('mapper') != -1) {
                    debugger;
                    var apiurl = self.selectedtransform;
                    $http({method: 'OPTIONS', url: apiurl}).then(function (data) {
                        debugger;
                        if (data.data.actions) {
                            var datab = data.data.actions.POST;
                            self.databkeys = Object.keys(datab);
                            self.MapperOptions = {};

                            debugger;
                        }
                    });

                }

            }


            self.getMapperList = function () {
                if (self.selectedtransform && self.selectedtransform.indexOf('mapper') != -1) {
                    //asegura que trabajamos con un mapper


                    var apiurl = self.selectedtransform;

                    $http.get(apiurl).then(function successCallback(response) {

                        if (response.data.results) {
                            self.MapperList = response.data.results;
                        }


                    }, function errorCallback(response) {
                        //Error en la recogida de datos
                    });

                }
                self.MapperList = null;

            }
        }]

    }
);
