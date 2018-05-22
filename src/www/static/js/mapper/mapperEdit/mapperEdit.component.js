(function (angular) {
    'use strict';

    angular
        .module('app.mapper')
        .component('mapperEdit', mapperEdit());

    function mapperEdit() {
        let component = {
            templateUrl: '/static/js/mapper/mapperEdit/mapperEdit.component.html',
            controller: MapperEditController,
            controllerAs: 'vm',
            bindings: {
                mapper: '<',
            }
        }
        return component;
    }

    function MapperEditController() {
        let vm = this;
        vm.$onInit = onInit;

        function onInit() {
            vm.data = parseObject(vm.mapper);
        }

        function parseObject(obj) {
            let data = {};
            for (let k in obj) {
                if (k === 'id') {
                    continue;
                } else if (typeof (obj[k]) === 'object' && obj[k]) {
                    let tmp = parseObject(obj[k]);
                    for (let t in tmp) {
                        data[`${k}.${t}`] = tmp[t];
                    }
                } else {
                    data[k] = obj[k];
                }
            }
            return data;
        }
    }

})(window.angular);
