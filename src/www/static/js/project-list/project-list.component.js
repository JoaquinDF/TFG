'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.
  module('projectList').
  component('projectList', {

    templateUrl: '/static/templates/project-list.template.html',
    controller: ['$http', function ProjectListController($http) {
      var self = this;

      $http.get('/api/v1/data/project/').then(function(response) {

        self.projects = response.data.results;
                debugger;

      });
    }]

  });
