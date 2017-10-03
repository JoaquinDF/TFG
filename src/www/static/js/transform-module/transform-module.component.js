'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.module('transformModule').component('transformModule', {

        templateUrl: '/static/templates/transform-module.template.html',
        controller: ['$http', '$timeout', function adminController($http, $timeout) {
            var self = this;
            self.MapperOptions = {};
            self.transforms = {};
            $http.get('/api/v1/transform/').then(function successCallback(response) {

                if (response.data) {
                    var todelete = [];
                    self.transforms = response.data;
                    for (var key in self.transforms) {
                        if (self.transforms[key].indexOf('delete') != -1 || self.transforms[key].indexOf('mapping') != -1) {
                            todelete.push(key);
                        }
                    }
                    for (var key in todelete) {
                        delete self.transforms[todelete[key]];
                    }

                } else {

                }

            }, function errorCallback(response) {
            });


            self.LaunchMapping = function () {

                var apiurl = self.selectedtransform;
                apiurl = apiurl.replace('mapper', 'mapping');

                var emptyjsontopost = {};

                $http.post(apiurl, emptyjsontopost).then(function successCallback(response) {

                    self.warning = 'CORRECT';
                }, function errorCallback(response) {
                    self.warning = 'ERROR'

                });
                self.MapperOptions = {};

            }

            self.LoadMapper = function () {

                var apiurl = self.selectedtransform;


                $http.post(apiurl, self.MapperOptions).then(function successCallback(response) {

                    self.getMapperList();
                    self.warning = 'CORRECT';

                }, function errorCallback(response) {
                    self.warning = 'ERROR'

                });
                self.MapperOptions = {};


            }
            self.setWarningSch = function () {
                $timeout(function () {
                    self.warning = null;
                }, 1500);


            }
            self.deletekey = function (id) {

                var object = {id: id};
                var apiurl = self.selectedtransform;
                apiurl = apiurl.replace('transform/', 'transform/delete')
                self.MapperOptions = {};


                $http.post(apiurl, object).then(function successCallback(response) {

                    self.getMapperList();

                }), function errorCallback(response) {
                    self.warning = 'ERROR'

                }

            }

            self.getMapperOptions = function () {
                if (self.selectedtransform && self.selectedtransform.indexOf('mapper') != -1) {

                    self.databkeys = [];
                    self.nestedkey = [];
                    var apiurl = self.selectedtransform;
                    $http({method: 'OPTIONS', url: apiurl}).then(function (data) {

                        if (data.data.actions) {
                            var datab = data.data.actions.POST;
                            Object.keys(datab).forEach(function (key) {


                                if (datab[key]['type'].indexOf('nested object') != -1) {
                                    self.nesteditems = Object.keys(datab[key]['children']);
                                    self.nestedkey.push(key, self.nesteditems.length)
                                    self.databkeys.push(key);

                                } else {
                                    self.databkeys.push(key);
                                }
                            });


                        }

                        self.MapperOptions = {};


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
