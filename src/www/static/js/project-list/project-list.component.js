'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.
  module('projectList').
  component('projectList', {

    templateUrl: '/static/templates/project-list.template.html',
    controller: ['$http', function ProjectListController($http , $scope) {
      var self = this;

      $http.get('/api/v1/extract/data/?collection=data.projects&limit=10&offset=0').then(function(responseprojects) {

        self.projects = responseprojects.data.results;
        self.projectsnext = responseprojects.data.next;
        self.projectsprev = responseprojects.data.previous;
        self.countprojects = responseprojects.data.count;
        self.currentpage = 0;
        self.nextproject = function () {
            if(self.projectsnext) {
                $http.get(self.projectsnext).then(function (responseprojects) {
                    debugger;
                    if (responseprojects.data) {
                        self.projects = responseprojects.data.results;
                        self.projectsnext = responseprojects.data.next;
                        self.projectsprev = responseprojects.data.previous;
                        self.currentpage+=1;
                    }
                });
            }
        }
        self.prevproject = function () {
          if(self.currentpage>0) {
                $http.get(self.projectsprev).then(function (responseprojects) {
                    if (responseprojects.data) {
                        self.projects = responseprojects.data.results;
                        self.projectsnext = responseprojects.data.next;
                        self.projectsprev = responseprojects.data.previous;
                        self.currentpage-=1;

                    }
                });
            }
        }


        self.changepage = function (page) {
            if(!isNaN(page) && page && page<self.countprojects) {

                var http = "/api/v1/extract/data/?collection=data.projects&limit=10&offset=" + page;
                debugger;
                console.log(http);
                $http.get(http).then(function (responseprojects) {
                    if (responseprojects.data) {

                        self.projects = responseprojects.data.results;
                        self.projectsnext = responseprojects.data.next;
                        self.projectsprev = responseprojects.data.previous;
                        self.page = page;
                        self.currentpage=parseInt(page);
                        debugger;
                    }
                });
            }
        }

      });

        $http.get('/api/v1/extract/data/?collection=data.calls').then(function(responsecalls) {

        self.calls = responsecalls.data.results;

      });

         $http.get('/api/v1/extract/data/?collection=data.organizations').then(function(responseorgs) {

        self.organizations = responseorgs.data.results;


      });
        $http.get('/api/v1/extract/data/?collection=data.project-call').then(function(responseprojectcalls) {

        self.projectcall = responseprojectcalls.data.results;

      });
        $http.get('/api/v1/data/projectorganization/').then(function(responseprojectorgs) {

        self.projectorgs = responseprojectorgs.data.results;

      });



    }]

  }

);