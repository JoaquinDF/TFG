'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.module('transformModule').component('transformModule', {

        templateUrl: '/static/templates/transform-module.template.html',
        controller: ['$http', '$timeout', function adminController($http, $timeout) {
            var self = this;
            self.selectedtransform;

            $http.get('/api/v1/transform/').then(function (responsetasks) {

                if (responsetasks.data) {

                    self.transforms = responsetasks.data
                    debugger;


                } else {
                }

            });


        }]

    }
);
