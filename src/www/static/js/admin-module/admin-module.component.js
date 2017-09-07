'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.module('adminModule').component('adminModule', {

        templateUrl: '/static/templates/admin-module.template.html',
        controller: ['$http', function ProjectListController($http, $scope) {
            var self = this;

        }]

    }
);
