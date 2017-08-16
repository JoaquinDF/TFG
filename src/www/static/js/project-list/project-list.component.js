'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.module('projectList').component('projectList', {

        templateUrl: '/static/templates/project-list.template.html',
        controller: ['$http', function ProjectListController($http, $scope) {
            var self = this;
            $http.get('/api/v1/extract/data/?collection=data.projects&limit=10&offset=0').then(function (responseprojects) {

                self.projects = responseprojects.data.results;
                self.projectsnext = responseprojects.data.next;
                self.projectsprev = responseprojects.data.previous;
                self.countprojects = Math.floor((responseprojects.data.count) / 10);
                self.pagecounter;
                self.currentpage = 0;
                self.nextproject = function () {
                    if (self.projectsnext) {
                        $http.get(self.projectsnext).then(function (responseprojects) {

                            if (responseprojects.data) {

                                self.projects = responseprojects.data.results;
                                self.projectsnext = responseprojects.data.next;
                                self.projectsprev = responseprojects.data.previous;
                                self.currentpage += 1;
                                 self.pagecounter=null;
                            }
                        });
                    }
                }
                self.prevproject = function () {
                    if (self.currentpage > 0) {
                        $http.get(self.projectsprev).then(function (responseprojects) {
                            if (responseprojects.data) {
                                self.projects = responseprojects.data.results;
                                self.projectsnext = responseprojects.data.next;
                                self.projectsprev = responseprojects.data.previous;
                                self.currentpage -= 1;
                                 self.pagecounter=null;

                            }
                        });
                    }
                }


                self.changepage = function (page) {
                    if (!isNaN(page) && page && page < self.countprojects) {
                       self.currentpage = parseInt(page);

                        page *= 10;
                        var http = "/api/v1/extract/data/?collection=data.projects&limit=10&offset=" + page;

                        console.log(http);
                        $http.get(http).then(function (responseprojects) {
                            if (responseprojects.data) {

                                self.projects = responseprojects.data.results;
                                self.projectsnext = responseprojects.data.next;
                                self.projectsprev = responseprojects.data.previous;

                            }
                        });
                    }
                }

            });


        }]

    }
);
