'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.module('forecastingModule').component('recommenderModule', {

        templateUrl: '/static/templates/recommender.template.html',

        controller: ['$http', '$window', function forecastingController($http, $window) {


            var ShowLoader = function () {
                document.getElementById('loader').style.display = ''
            }

            var HideLoader = function () {
                document.getElementById('loader').style.display = 'none'

            }
            var ShowLoader = function () {
                document.getElementById('loader').style.display = ''

            }

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

            self.keydown = function (keyEvent) {
                console.log('keydown -' + keyEvent);
                if (keyEvent.key == 'Enter') {

                    self.check();
                }
            }
            self.check = function () {
                self.data = {
                    "search": self.search,
                    "presupuesto": self.presupuesto,
                    "subvencion": self.subvencion,
                    "country": self.pais,
                    "startdate": new Date(self.startdate).valueOf()
                }

                $('#ModalLoader').modal('show')

                $http.post('/api/v1/data/GetRecommendation/', self.data).then(function successCallback(response) {
                    self.resultGlobal = response.data.resultGlobal == 1 ? "SI" : "NO";
                    self.resultSubPres = response.data.resultSubPres == 1 ? "SI" : "NO";
                    self.image = response.data.image;
                    debugger;
                    $('#ModalLoader').modal('hide')
                    $('#myModal').modal('show')

                    debugger;


                }, function errorCallback(response) {


                });


            }


        }]

    }
);