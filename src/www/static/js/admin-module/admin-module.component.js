'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.module('adminModule').component('adminModule', {

        templateUrl: '/static/templates/admin-module.template.html',
    controller: ['$http', '$timeout', function adminController($http, $timeout) {
            var self = this;

        $http.get('/api/v1/admin/listTask/').then(function (responsetasks) {

            if (responsetasks.data) {

                self.tasks = responsetasks.data;


            } else {
                self.tasks = null;
            }

        });


            $http.get('/api/v1/admin/listCrawlers/').then(function (responsecrawlers) {

                if (responsecrawlers.data) {

                    self.crawlers = responsecrawlers.data;

                } else {
                    self.crawlers = null;
                }

            });
            $http.get('/api/v1/admin/listBots/').then(function (responsebots) {

                if (responsebots.data) {

                    self.bots = responsebots.data;

                } else {
                    self.bots = null;
                }
            });

        self.warning = null;
        this.intervalperiod = ['days',
            , 'hours'
            , 'minutes'
            , 'seconds'
            , 'microseconds'];

        this.objectTask = {
            task: '',
            args: '',
            interval: null,
            crontab: null,
            intervalevery: '',
            intervalperiod: '',
            minute: null,
            hour: null,
            day_of_week: null,
            day_of_month: null,
            month_of_year: null
        };

            self.settask = function () {

                $http.post('/api/v1/admin/periodicTask/', this.objectTask).then(function successCallback(response) {

                    self.warning = 'CORRECT';
                }, function errorCallback(response) {
                    self.warning = 'ERROR'

                });


            }

            self.getschedule = function () {
                $http.get('/api/v1/admin/schedule/').then(function (responsecrawlers) {

                    if (responsecrawlers.data) {

                        self.schedule = responsecrawlers.data;

                    } else {
                        self.schedule = null;
                    }

                });
            }

            self.setWarningSch = function () {
                $timeout(function () {
                    self.warning = null;
                    self.getschedule()
                }, 750);


            }


            self.setinterval = function () {
                self.objectTask.interval = true;
                self.objectTask.crontab = null;
                self.warning = null;
            }
            self.setcrontab = function () {
                self.objectTask.interval = null;
                self.objectTask.crontab = true;
                self.warning = null;

            }
            self.deleteTask = function (name) {
                var json = {name: name};
                $http.post('/api/v1/admin/deleteTask/', json).then(function successCallback(response) {

                    self.warning = 'CORRECT';
                }, function errorCallback(response) {
                    self.warning = 'ERROR'

                });
            }

        self.getschedule();

        }]

    }
);
