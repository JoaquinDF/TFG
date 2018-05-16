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
            self.textcount = 0;
            $http.get('/api/v1/data/ListCountriesAvailable/').then(function successCallback(response) {

                self.countries = response.data;

            }, function errorCallback(response) {
                console.log("Error on ListCountriesAvailable")

            });

            self.wordcount = function () {
                var s = self.search;
                if (s != undefined) {
                    s = s.replace(/(^\s*)|(\s*$)/gi, "");
                    s = s.replace(/[ ]{2,}/gi, " ");
                    s = s.replace(/\n /, "\n");
                    self.textcount = s.split(' ').length;
                    console.log(self.textcount)
                    if (self.textcount <= 100) {
                        $("#countError").css("display", '');

                    } else {
                        $("#countError").css("display", 'none');

                    }
                } else {
                    self.search = "";
                    $("#countError").css("display", '');

                }
            }
            self.keydown = function (keyEvent) {

                if (keyEvent.key && keyEvent.key == 'Enter') {
                    console.log('keydown -' + keyEvent);
                    self.check();
                }


            }


            self.competence = function () {
                var url = "/www/#!" + '/forecasting/' + self.search
                $window.location.href = url
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
