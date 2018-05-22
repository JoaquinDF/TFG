(function (angular) {
    'use strict';

    angular
        .module('app.admin')
        .component('adminNavbar', adminNavbar());

    function adminNavbar() {
        var component = {
            templateUrl: '/static/js/admin/adminNavbar/adminNavbar.component.html',
        };
        return component;
    }

})(window.angular);