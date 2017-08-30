/**
 * Created by JoaquinDF on 28/7/17.
 */
'use strict';

var Appmodule = angular.module('innhomeweb', [
    'projectList',
    'callList',
    'organizationList',
    'searchList',


]);


 Appmodule
.controller('MainCtrl', ['$scope', '$location',
                        function ($scope,$location) {
 $scope.redirectTo = function(from,where){
     $location.url("'/www/search/' + from + '-' + where");
 }
    }]);