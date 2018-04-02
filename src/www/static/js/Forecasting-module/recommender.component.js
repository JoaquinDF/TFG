'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.module('forecastingModule').component('recommenderModule', {

        templateUrl: '/static/templates/recommender.template.html',

        controller: ['$http', '$window', function forecastingController($http, $window) {

            var self = this;
            self.search = "";
            self.startdate = "";
            self.presupuesto = "";
            self.subvención = "";
            self.countries = "";

            $http.get('/api/v1/data/ListCountriesAvailable/').then(function successCallback(response) {

                self.countries = response.data;

            }, function errorCallback(response) {
                console.log("Error on ListCountriesAvailable")

            });


            self.check = function () {
                self.data = {
                    "presupuesto": self.presupuesto,
                    "subvencion": self.subvención,
                    "country": self.countries,
                    "startdate": self.startdate
                }
                $http.post('/api/v1/data/CommunityEstimation/', self.data).then(function successCallback(response) {
                    document.getElementById('entry').style.height = "100px"
                    document.getElementById('loader').style.display = 'none'
                    document.getElementById('sigma-container').style.display = ''

                    self.estimation = response.data;
                    self.loadgraph(self.estimation)
                    debugger;

                }, function errorCallback(response) {


                });


            }


        }]

    }
);
