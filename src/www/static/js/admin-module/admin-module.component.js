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
            this.intervalperiod = ['IntervalSchedule.DAYS',
'IntervalSchedule.HOURS',
'IntervalSchedule.MINUTES',
'IntervalSchedule.SECONDS',
'IntervalSchedule.MICROSECONDS']

             this.objectTask = {task:'', args:'', interval:null, crontab:null ,intervalevery:'', intervalperiod:''  , minute: null, hour: null , day_of_week: null, day_of_month: null, month_of_year: null};

            self.settask = function () {

                $http.post('/api/v1/admin/PeriodicTask/',this.objectTask).then(function successCallback(response) {
                debugger;

                    self.warning='CORRECT';
                }, function errorCallback(response) {
                    self.warning = 'ERROR'
                                    debugger;

              });




            }


            self.setinterval = function () {
                self.objectTask.interval=true;
                self.objectTask.crontab=null;
                self.warning=null;
                debugger;
            }
            self.setcrontab = function () {
                self.objectTask.interval=null;
                self.objectTask.crontab=true;
                self.warning=null;

                debugger;
            }




        }]

    }
);
