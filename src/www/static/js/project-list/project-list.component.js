'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.
  module('projectList').
  component('projectList', {

    templateUrl: '/static/templates/project-list.template.html',
    controller: ['$http', function ProjectListController($http , $scope) {
      var self = this;

      $http.get('/api/v1/extract/data/?collection=data.projects&limit=10&offset=855').then(function(responseprojects) {

        self.projects = responseprojects.data.results;



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