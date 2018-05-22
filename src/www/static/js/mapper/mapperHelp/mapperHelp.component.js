(function (angular) {
    'use strict';

    angular
        .module('app.mapper')
        .component('mapperHelp', mapperHelp());

    function mapperHelp() {
        let component = {
            templateUrl: '/static/js/mapper/mapperHelp/mapperHelp.component.html',
        };
        return component;
    }
})(window.angular);