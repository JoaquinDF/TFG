'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.module('forecastingModule').component('recommenderModule', {

        templateUrl: '/static/templates/recommender.template.html',

        controller: ['$http', '$window', function forecastingController($http, $window) {

            var self = this;
            self.search = "";
            self.pais = "";
            self.startdate = "";
            self.presupuesto = "";
            self.subvencion = "";
            self.countries = "";

            $http.get('/api/v1/data/ListCountriesAvailable/').then(function successCallback(response) {

                self.countries = response.data;

            }, function errorCallback(response) {
                console.log("Error on ListCountriesAvailable")

            });


            self.check = function () {
                self.data = {
                    "search": self.search,
                    "presupuesto": self.presupuesto,
                    "subvencion": self.subvencion,
                    "country": self.pais,
                    "startdate": new Date(self.startdate).valueOf()
                }
                $http.post('/api/v1/data/GetRecommendation/', self.data).then(function successCallback(response) {

                    debugger;

                }, function errorCallback(response) {


                });


            }


        }]

    }
);
