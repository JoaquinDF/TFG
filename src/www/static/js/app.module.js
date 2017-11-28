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

            .when('/p:id', {template: ' <search-list style="display: flex"></search-list>'})
            .when('/np:id', {template: ' <search-list style="display: flex"></search-list>'})
            .when('/c:id', {template: ' <search-list style="display: flex"></search-list>'})
            .when('/nc:id', {template: ' <search-list style="display: flex"></search-list>'})
            .when('/o:id', {template: ' <search-list style="display: flex"></search-list>'})
            .when('/no:id', {template: ' <search-list style="display: flex"></search-list>'})


            .when('/search', {
                template: '<search-list style="display: flex"></search-list>'
            })

            .when('/metric', {
                template: '<metric-module style="display: flex"></metric-module>'
            })

            .when('/metric:id', {
                template: '<metric-module style="display: flex"></metric-module>'
            })
    }]);

