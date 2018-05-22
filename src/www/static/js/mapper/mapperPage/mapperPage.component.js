(function (angular) {
    'use strict';

    angular
        .module('app.mapper')
        .component('mapperPage', mapperPage());

    function mapperPage() {
        let component = {
            templateUrl: '/static/js/mapper/mapperPage/mapperPage.component.html',
            controller: MapperPageController,
            controllerAs: 'vm'
        };
        return component;
    }

    MapperPageController.$inject = [
        'mapperService'
    ];

    function MapperPageController(mapperService) {
        let vm = this;
        vm.$onInit = onInit;

        function onInit() {
            mapperService.getMappersUrls()
                .then(data => vm.mapperPage = data);
        }
    }
})(window.angular);