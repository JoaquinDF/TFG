(function (angular) {
    'use strict';

    angular
        .module('app.mapper')
        .component('mapperLaunch', mapperLaunch());

    function mapperLaunch() {
        let component = {
            templateUrl: '/static/js/mapper/mapperLaunch/mapperLaunch.component.html',
            controller: MapperLaunchController,
            controllerAs: 'vm',
            bindings: {
                mapper: '<'
            }
        };
        return component;
    }

    function MapperLaunchController() {

    }
})(window.angular);