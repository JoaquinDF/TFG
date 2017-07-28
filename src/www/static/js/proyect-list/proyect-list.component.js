'use strict';

// Register `proyectList` component, along with its associated controller and template!
angular.
  module('ProyectList').
  component('proyectList', {

    templateUrl: 'templates/templates.proyect_list-template.html',
    controller: ['$http', function ProyectListController($http) {
        debugger;
      var self = this;

      $http.get('/api/v1/data/project/').then(function(response) {

        self.proyects = response.data;
      });
    }]

  });
