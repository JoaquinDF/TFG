'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.module('adminModule').component('adminModule', {

        templateUrl: '/static/templates/admin-module.template.html',
        controller: ['$http', function ProjectListController($http, $scope) {
            var self = this;
            self.warning=null;
             this.objectTask = {option: 'crontabs' , minute: null, hour: null , day_of_week: null, day_of_month: null, month_of_year: null};

            self.settask = function () {

                $http.post('/api/v1/admin/crontabs/',this.objectTask).then(function successCallback(response) {
                debugger;

                    self.warning=null;
                }, function errorCallback(response) {
                self.warning = 'Warning!, Cannot Post the data!'
                                    debugger;

              });






            }



        }]

    }
);
