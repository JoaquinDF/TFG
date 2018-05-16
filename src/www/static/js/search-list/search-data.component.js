'use strict';

// Register `countList` component, along with its associated controller and template!
angular.module('searchList').component('searchData', {

    templateUrl: '/static/templates/search-data.template.html',
    controller: ['$http', function CallsListController($http, $scope) {
        var self = this;
        self.textsearch = ""
        self.selectsearch = ""
        self.modeofsearch = ""
        self.relatedCollection = ""
        self.toPost = ""
        self.datasearch = ""
        self.tofind = function () {

            var model = self.selectsearch.slice(0, 1)
            var field = self.selectsearch.slice(1, -1) + "__" + self.modeofsearch + '=';
            var data = self.textsearch;
            self.toPost = field + data;
            if (model === 'p') self.relatedCollection = 'project';
            if (model === 'c') self.relatedCollection = 'call';
            if (model === 'o') self.relatedCollection = 'organization';


            $http.get('/api/v1/data/' + self.relatedCollection + '/' + self.toPost + '&limit=10&offset=0').then(function (responsesearch) {

                self.datasearch = responsesearch.data.results;
                self.searchnext = responsesearch.data.next;
                self.searchprev = responsesearch.data.previous;
                self.countsearch = Math.floor(((responsesearch.data.count) / 10) + 1);
                self.currentpagesearch = 1;
            });


        }
        self.startingsearch = function () {

            $http.get('/api/v1/data/' + self.relatedCollection + '/' + self.toPost + '&limit=10&offset=0').then(function (responsesearch) {

                self.datasearch = responsesearch.data.results;
                self.searchnext = responsesearch.data.next;
                self.searchprev = responsesearch.data.previous;
                self.countsearch = Math.floor(((responsesearch.data.count) / 10) + 1);
                self.currentpagesearch = 1;
            });

        }

        self.nextsearch = function () {
            if (self.searchnext) {
                $http.get(self.searchnext).then(function (responsesearch) {

                    if (responsesearch.data) {

                        self.datasearch = responsesearch.data.results;
                        self.searchnext = responsesearch.data.next;
                        self.searchprev = responsesearch.data.previous;
                        self.currentpagesearch += 1;
                    }
                });
            }


        }

        self.onHoverMetrics = function (organization) {
            if (!organization) return false;
            var country = organization.direccion.pais;

            var http = "/api/v1/data/RegionMetric/?region=" + country;

            $http.get(http).then(function (responseorganizations) {
                if (responseorganizations.data) {

                    var data = responseorganizations.data.results[0];

                    self.regionName = data.country;
                    self.numeroProyectosR = data.numeroProyectos;
                    self.porcentajesubvencionadoR = (parseFloat(data.porcentajesubvencionado)).toFixed(1);
                    self.numeroProyectosMedioR = (parseFloat(data.numeroProyectos) / parseFloat(data.numeroEmpresas)).toFixed(1);
                    self.numeroEmpresas = parseFloat(data.numeroEmpresas)

                    var http = "/api/v1/data/OrganizationMetric/?organization=" + organization.id;

                    $http.get(http).then(function (responseorganizations) {
                        if (responseorganizations.data) {

                            var data = responseorganizations.data.results[0];

                            self.porcentajesubvencionadoO = (parseFloat(data.porcentajeSubvencionado)).toFixed(1);
                            self.numeroProyectosO = data.numeroProyectos;


                            self.porcentajeRelativo = ((self.porcentajesubvencionadoO / self.porcentajesubvencionadoR)).toFixed(1);
                            self.proyectosRelativo = (self.numeroProyectosO - self.numeroProyectosMedioR).toFixed(1)


                        }


                    });

                }

            });


        }

        self.lastsearch = function () {
            var page = self.currentpagesearch;
            page *= 10;
            page -= 10;
            var apitogo = '/api/v1/data/' + self.relatedCollection + '/' + self.toPost + '&limit=10&offset=' + page;
            $http.get(apitogo).then(function (responsesearch) {

                self.datasearch = responsesearch.data.results;
                self.currentpagesearch = responsesearch.data.next;
                self.searchprev = responsesearch.data.previous;
                self.currentpagesearch = self.countsearch;
            });
        }

        self.prevsearch = function () {
            if (self.currentpagesearch > 1) {
                $http.get(self.searchprev).then(function (responsesearch) {
                    if (responsesearch.data) {
                        self.datasearch = responsesearch.data.results;
                        self.searchnext = responsesearch.data.next;
                        self.searchprev = responsesearch.data.previous;
                        self.currentpagesearch -= 1;

                    }
                });
            }
        }

    }]
});