'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.module('transformModule').component('transformModule', {

        templateUrl: '/static/templates/transform-module.template.html',
        controller: ['$http', '$timeout', function adminController($http, $timeout) {
            var self = this;

            $http.get('/api/v1/transform/').then(function successCallback(response) {

                if (response.data) {

                    self.transforms = response.data


                } else {

                }

            }, function errorCallback(response) {
                //Error en la recogida de datos.
            });


            self.getMapperOptions = function () {
                if (self.selectedtransform && self.selectedtransform.indexOf('mapper') != -1) {
                    debugger;
                    var apiurl = self.selectedtransform;
                    $http({method: 'OPTIONS', url: apiurl}).then(function (data) {
                        debugger;
                        if (data.data.actions) {
                            var datab = data.data.actions.POST;
                            self.databkeys = Object.keys(datab);
                            self.MapperOptions = JSON.stringify(self.databkeys);

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
