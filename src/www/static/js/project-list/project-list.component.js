'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.module('projectList').component('projectList', {

    templateUrl: '/static/templates/project-list.template.html',
    controller: ['$http', function ProjectListController($http, $scope) {
        var self = this;

        self.projectfind = ""

        self.startingproject = function () {

            $http.get('/api/v1/data/project/?limit=10&offset=0&ordering=tituloProyecto').then(function (responseprojects) {

                self.projects = responseprojects.data.results;
                self.projectsnext = responseprojects.data.next;
                self.projectsprev = responseprojects.data.previous;
                self.countprojects = Math.floor(((responseprojects.data.count) / 10) + 1);
                self.currentpage = 1;
            });
        }

        self.nextproject = function () {
            if (self.projectsnext) {
                $http.get(self.projectsnext).then(function (responseprojects) {

                    if (responseprojects.data) {

                        self.projects = responseprojects.data.results;
                        self.projectsnext = responseprojects.data.next;
                        self.projectsprev = responseprojects.data.previous;
                        self.currentpage += 1;
                    }
                });
            }


        }

        self.lastproject = function () {
            var page = self.countprojects;
            page *= 10;
            page -= 10;
            var apitogo = "/api/v1/data/project/?limit=10&offset=" + page + "&ordering=tituloProyecto";
            $http.get(apitogo).then(function (responseprojects) {

                self.projects = responseprojects.data.results;
                self.projectsnext = responseprojects.data.next;
                self.projectsprev = responseprojects.data.previous;
                self.currentpage = self.countprojects;
            });
        }

        self.prevproject = function () {
            if (self.currentpage > 1) {
                $http.get(self.projectsprev).then(function (responseprojects) {
                    if (responseprojects.data) {
                        self.projects = responseprojects.data.results;
                        self.projectsnext = responseprojects.data.next;
                        self.projectsprev = responseprojects.data.previous;
                        self.currentpage -= 1;
                        self.pagecounter = null;

                    }
                });
            }
        }


        self.changepage = function (page) {
            if (!isNaN(page) && page && page < self.countprojects) {
                self.currentpage = parseInt(page);

                page *= 10;
                page -= 10;
                var http = "/api/v1/data/project/?limit=10&offset= " + page + "&ordering=tituloProyecto";

                $http.get(http).then(function (responseprojects) {
                    if (responseprojects.data) {

                        self.projects = responseprojects.data.results;
                        self.projectsnext = responseprojects.data.next;
                        self.projectsprev = responseprojects.data.previous;

                    }
                });
            }
        }

        self.findProject = function (toFind) {
            if ((toFind != "") && toFind) {
                self.projectfind = toFind
                var http = "/api/v1/data/project/?limit=10&offset=0&ordering=tituloProyecto&name=" + toFind;

                $http.get(http).then(function (responseprojects) {
                    if (responseprojects.data) {

                        self.projects = responseprojects.data.results;
                        self.projectsnext = responseprojects.data.next;
                        self.projectsprev = responseprojects.data.previous;
                        self.countprojects = Math.floor(((responseprojects.data.count) / 10) + 1);
                        self.pagecounter;
                        self.currentpage = 1;
                    }
                });
            } else {

                self.startingproject()


            }

        }

        self.saveedit = function () {
            var keys = Object.keys(self.EditProject);
            var tosave = {}


            for (var key in keys) {
                tosave[keys[key]] = $('#' + keys[key]).val()
            }
            tosave['keys'] = keys.join()

            $http.put('/api/v1/data/project/' + self.EditProject['id'] + '/', tosave).then(function successCallback(response) {

                self.findProject(self.projectfind)

            }, function errorCallback(response) {

                debugger;
            });


        }


        self.editProject = function (idtoEdit) {
            self.EditProject = [];
            var http = "/api/v1/data/project/?id=" + idtoEdit;
            $http.get(http).then(function (responseprojects) {
                if (responseprojects.data) {

                    self.EditProject = responseprojects.data.results[0];
                    $('#editProject').modal('show')

                }
            });


        }

        self.startingproject();


    }]

});