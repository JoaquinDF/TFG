/**
 * Created by JoaquinDF on 28/7/17.
 */
'use strict';


var Appmodule = angular.module('innhomeweb', [
    'dataList',
    'projectList',
    'callList',
    'organizationList',
    'searchList',
    'metricModule',
    'ngRoute',
    'datamaps',
    'forecastingModule',
    'parallelsModule',
    'mapsModule',
    'communityModule',
    'app.admin'
]);

Appmodule.config(['$locationProvider', '$routeProvider',
    function config($locationProvider, $routeProvider) {
        $locationProvider.hashPrefix('!');
        $routeProvider
            .when('/project', {
                template: '<project-list></project-list>',


            })
            .when('/',
                {
                    template: '<start-list></start-list>'
                })
            .when('/organization', {
                template: '<organization-list></organization-list>'
            })
            .when('/call', {
                template: '<call-list></call-list>'
            })


            .when('/search', {
                template: '<search-data style="display: block"></search-data>'
            })

            .when('/metric', {
                template: '<metric-module style="display: block "></metric-module>'
            })

            .when('/metric:id', {
                template: '<metric-module style="display: block"></metric-module>'
            })
            .when('/forecasting', {
                template: '<forecasting-module style="display: block"></forecasting-module>'
            })
            .when('/forecasting/:data', {
                template: '<forecasting-module style="display: block"></forecasting-module>'
            })
            .when('/admin', {
                template: '<admin-navbar></admin-navbar>'

            })
            .when('/recommender', {
                template: '<recommender-module style="display: block"></recommender-module>'
            })
            .when('/maps/:map', {
                templateUrl: '/static/templates/maps-metric-module.template.html',
                controller: 'ControladorMaps'
            })

            .when('/community/:group/', {
                templateUrl: '/static/templates/community-module.template.html',
                controller: 'COMMUNITY'
            })
            .when('/parallels', {

                templateUrl: '/static/templates/parallels-module.template.html',
                controller: 'PARALLELS'
            })


            .when('/parallels/:id/', {

                templateUrl: '/static/templates/parallels-module.template.html',
                controller: 'PARALLELS'
            })
            .when('/data', {template: '<start-list></start-list>'})
            .when('/p:id', {template: ' <search-list style="display: flex"></search-list>'})
            .when('/np:id', {template: ' <search-list style="display: flex"></search-list>'})
            .when('/c:id', {template: ' <search-list style="display: flex"></search-list>'})
            .when('/nc:id', {template: ' <search-list style="display: flex"></search-list>'})
            .when('/o:id', {template: ' <search-list style="display: flex"></search-list>'})
            .when('/no:id', {template: ' <search-list style="display: flex"></search-list>'})

    }]);


Appmodule.controller('HandleSearchEvents', ['$scope', '$http', function ($scope, $http) {

    $scope.helloworld = "HI!";
    $scope.textmetric = "";
    $scope.onMetricEnter = function (url1, where) {

        if (where == "orgs") {
            if (url1 == "") {
                $scope.Orgs = []

            } else {

                var apiget = '/api/v1/data/organization/?format=json&name=' + url1;
                $scope.Orgs;
                $http.get(apiget).then(function successCallback(response) {
                    $scope.Orgs = (response.data.results)
                    if ($scope.Orgs.length > 5) {
                        debugger
                        $scope.Orgs = $scope.Orgs.slice(0, 5)
                    }
                    debugger;

                });
            }


        } else if (where == "proy") {
            if (url1 == "") {
                $scope.Proyectos = []

            } else {

                var apiget = '/api/v1/data/project/?format=json&name=' + url1;

                $scope.Proyectos;
                $http.get(apiget).then(function successCallback(response) {
                    $scope.Proyectos = (response.data.results)
                    if ($scope.Proyectos.length > 5) {
                        debugger
                        $scope.Proyectos = $scope.Proyectos.slice(0, 5)
                    }
                    debugger;

                });
            }

        } else if (where == "call") {
            if (url1 == "") {
                $scope.Calls = []

            } else {

                var apiget = '/api/v1/data/call/?format=json&name=' + url1;

                $scope.Calls;
                $http.get(apiget).then(function successCallback(response) {
                    $scope.Calls = (response.data.results)
                    if ($scope.Calls.length > 5) {
                        debugger
                        $scope.Calls = $scope.Calls.slice(0, 5)
                    }
                    debugger;

                });
            }

        }


    }

    $scope.debug = function (a, b) {
        debugger;

    }
}])

