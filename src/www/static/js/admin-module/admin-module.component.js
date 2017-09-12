'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.module('adminModule').component('adminModule', {

        templateUrl: '/static/templates/admin-module.template.html',
        controller: ['$http', function adminController($http, $scope) {
            var self = this;

           $http.get('/api/v1/admin/listTask/').then(function (responsetasks) {

                        if (responsetasks.data) {

                            self.tasks=responsetasks.data;

                            debugger;
                        }else {
                            self.tasks = null;
                        }

                    });

                        $http.get('/api/v1/admin/listCrawlers/').then(function (responsecrawlers) {

                        if (responsecrawlers.data) {

                            self.crawlers=responsecrawlers.data;

                            debugger;
                        }else {
                            self.crawlers = null;
                        }

                    });
                        $http.get('/api/v1/admin/listBots/').then(function (responsebots) {

                        if (responsebots.data) {

                            self.bots=responsebots.data;

                            debugger;
                        }else {
                            self.bots = null;
                        }
                debugger;
                    });

            self.warning=null;
             this.objectTask = {task:'', args:'' ,option: 'crontabs' , minute: null, hour: null , day_of_week: null, day_of_month: null, month_of_year: null};

            self.settask = function () {

                $http.post('/api/v1/admin/PeriodicTask/',this.objectTask).then(function successCallback(response) {
                debugger;

                    self.warning=null;
                }, function errorCallback(response) {
                self.warning = 'Warning!  Cannot Post the data!'
                                    debugger;

              });






            }



        }]

    }
);
