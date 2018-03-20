/**
 * Created by JoaquinDF on 28/7/17.
 */
'use strict';


var Appmodule = angular.module('innhomeweb', [
    'projectList',
    'callList',
    'organizationList',
    'searchList',
    'adminModule',
    'transformModule',
    'metricModule',
    'ngRoute',
    'datamaps',
    'forecastingModule',
    'parallelsModule',
    'mapsModule',
    'communityModule',
]);

Appmodule.config(['$locationProvider', '$routeProvider',
    function config($locationProvider, $routeProvider) {
        $locationProvider.hashPrefix('!');
        $routeProvider
            .when('/project', {
                template: '<project-list></project-list>',


            })

            .when('/organization', {
                template: '<organization-list></organization-list>'
            })
            .when('/call', {
                template: '<call-list></call-list>'
            })
            .when('/admin', {
                template: '<admin-module style="display: flex; margin-top: 5%"></admin-module>'
            })

            .when('/transform', {
                template: ' <transform-module style="display: flex"></transform-module>'
            })


            .when('/search', {
                template: '<search-list style="display: block"></search-list>'
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
                $scope.Orgs = $scope.Orgs.clear();

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
                $scope.Proyectos = $scope.Proyectos.clear()

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


        }


    }

    $scope.debug = function (a, b) {
        debugger;

    }
}])

