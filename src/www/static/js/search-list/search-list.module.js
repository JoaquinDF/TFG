'use strict';

// Define the `projectList` module
var slist= angular.module('searchList', []);




slist.controller('DEBUG', ['$scope', function($scope) {

    $scope.debug = function (a,b) {


    }

     $scope.isobj = function (a) {
        return (angular.isObject(a))
    }

}]);
