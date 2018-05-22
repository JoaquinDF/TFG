(function (angular) {
    'use strict';

    angular
        .module('app.task')
        .component('taskHelp', taskHelp());

    function taskHelp() {
        let component = {
            templateUrl: '/static/js/task/taskHelp/taskHelp.component.html',
        };
        return component;
    }
})(window.angular);