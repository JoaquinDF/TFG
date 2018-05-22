(function (angular) {
    'use strict';

    angular
        .module('app.mapper')
        .component('mapperCreate', mapperCreate());

    function mapperCreate() {
        let component = {
            templateUrl: '/static/js/mapper/mapperCreate/mapperCreate.component.html',
            controller: CreateMapperController,
            controllerAs: 'vm',
            bindings: {
                options: '<'
            }
        };
        return component;
    }

    function CreateMapperController() {
        let vm = this;
        vm.$onInit = onInit;
        vm.$onChanges = onChanges;

        function onInit() {
            vm.template = parseOptions(vm.options);
        }

        function onChanges(changesObj) {
            if (changesObj.options) {
                vm.template = parseOptions(changesObj.options.currentValue)
            }
        }

        function parseOptions(opts) {
            let data = {}
            for (let k in opts) {
                if (k === 'id') {
                    continue;
                } else if ('children' in opts[k]) {
                    let tmp = parseOptions(opts[k].children);
                    for (let t in tmp) {
                        data[`${k}.${t}`] = undefined;
                    }
                } else {
                    data[k] = undefined;
                }
            }
            return data;
        }
    }
})(window.angular);