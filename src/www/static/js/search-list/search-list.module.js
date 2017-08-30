'use strict';

// Define the `projectList` module
var slist= angular.module('searchList', []);




slist.controller('DEBUG', ['$scope', function($scope) {

    $scope.debug = function (a,b) {
        console.log("Key= "+ a + " Value= " + b);
        debugger;

    }

     $scope.isobj = function (a) {
        if (angular.isObject(a)){
            debugger;
            return true;
        }return false;

    }
}]);
