(function (angular) {
    'use strict';

    angular
        .module('app.mapper')
        .factory('mapperService', mapperService);

    mapperService.$inject = [
        '$http'
    ];

    function mapperService($http) {
        let urlRoot = '/api/v1/';

        let service = {
            getMappersUrls: getMappersUrls,
            getMappers: getMappers,
            getOptions: getOptions
        };

        return service;

        function getMappersUrls() {
            return $http({
                method: 'GET',
                url: `${urlRoot}transform/`,
                cache: true
            })
                .then(parseMapperUrl)
                .catch(failed);
        }

        function getMappers(url) {
            return $http({
                method: 'GET',
                url: url,
                cache: true
            })
                .then(parseMapper)
                .catch(failed);
        }

        function getOptions(url) {
            return $http({
                method: 'OPTIONS',
                url: url,
                cache: true
            })
                .then(parseOptions)
                .catch(failed);
        }

        function parseMapperUrl(response) {
            let lst = [];
            let data = response.data;
            for (let k in data) {
                if (k.includes('mapper')) {
                    lst.push({
                        nombre: k,
                        url: data[k]
                    });
                }
            }
            return lst;
        }

        function parseMapper(response) {
            return response.data;
        }

        function parseOptions(response) {
            return response.data.actions.POST;
        }

        function failed(error) {
            console.error(error.data);
        }
    }
})(window.angular);