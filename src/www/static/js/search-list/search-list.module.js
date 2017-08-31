'use strict';

// Define the `projectList` module
var slist= angular.module('searchList', []);




slist.controller('DEBUG', ['$scope', function($scope) {

    $scope.debug = function (a,b) {
                debugger;


    }

     $scope.isobj = function (a) {
        return (angular.isObject(a))
    }

}]);
