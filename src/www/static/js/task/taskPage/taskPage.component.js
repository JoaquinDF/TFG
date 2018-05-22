(function (angular) {
    'use strict';

    angular
        .module('app.task')
        .component('taskPage', taskPage());

    function taskPage() {
        let component = {
            templateUrl: '/static/js/task/taskPage/taskPage.component.html',
            controller: TaskPageController,
            controllerAs: 'vm'
        };
        return component;
    }

    TaskPageController.$inject = [
        'taskService'
    ];

    function TaskPageController(taskService) {
        let vm = this;
        vm.$onInit = onInit;

        function onInit() {
            taskService.getPeriodicTasks()
                .then(data => vm.periodicTasks = data);
        }
    }
})(window.angular);