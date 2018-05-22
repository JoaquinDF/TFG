(function (angular) {
    'use strict';

    angular
        .module('app.task')
        .factory('taskService', mapperService);

    mapperService.$inject = [
        '$http'
    ];

    function mapperService($http) {
        let urlRoot = '/api/v1/';

        let service = {
            getPeriodicTasks: getPeriodicTasks,
        };

        return service;

        function getPeriodicTasks() {
            return $http({
                method: 'GET',
                url: `${urlRoot}admin/testperiodictask/`,
                cache: true
            })
                .then(parsePeriodicTasks)
                .catch(failed);
        }

        function parsePeriodicTasks(response) {
            return response.data;
        }

        function failed(error) {
            console.error(error.data);
        }
    }
})(window.angular);