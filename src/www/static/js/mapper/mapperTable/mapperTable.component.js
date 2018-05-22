(function (angular) {
    'use strict';

    angular
        .module('app.mapper')
        .component('mapperTable', mapperTable());

    function mapperTable() {
        let component = {
            templateUrl: '/static/js/mapper/mapperTable/mapperTable.component.html',
            controller: MapperTableController,
            controllerAs: 'vm',
            bindings: {
                nombre: '<',
                url: '<'
            }
        };
        return component;
    }

    MapperTableController.$inject = [
        'mapperService'
    ];

    function MapperTableController(mapperService) {
        let vm = this;
        this.$onInit = onInit;
        this.$onChanges = onChanges;
        this.onSiguiente = onSiguiente;

        function onInit() {
            setData(vm.url);
        }

        function onChanges(changesObj) {
            if (changesObj.url) {
                setData(changesObj.url.currentValue);
            }
        }

        function onSiguiente(url) {
            vm.url = url;
            setData(vm.url);
        }

        function setData(url) {
            mapperService.getMappers(url)
                .then(data => {
                    vm.mappers = data
                    let params = (new URL(url)).searchParams;
                    vm.page = params.get('offset') ? (params.get('offset') / params.get('limit')) + 1 : 1;
                    vm.total = Math.round((vm.mappers.count / 10) + 1); // TODO: Esto está mal, corregir
                });
            mapperService.getOptions(url)
                .then(data => vm.options = data);
        }
    }
})(window.angular);