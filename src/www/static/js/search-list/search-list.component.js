'use strict';

// Register `countList` component, along with its associated controller and template!
angular.module('searchList').component('searchList', {

        templateUrl: '/static/templates/search-list.template.html',
        controller: ['$http', function CallsListController($http, $scope) {
            var self = this;
              var x = document.URL;
              var projectid, callid,organizationid;
              var regex = new RegExp('\/(p|o|c)[0-9a-zA-Z]*');
              var tipo = regex.exec(x);
                debugger;
                if(tipo!=null) {
                    switch (tipo[1]) {
                        case 'p':
                            projectid = (tipo[0].split('/p'))[1];
                             var apiget = '/api/v1/data/project/?format=json&id=' + projectid;

                             $http.get(apiget).then(function successCallback(response) {
                                self.Proyecto=response.data.results;
                                debugger;

                            });



                            var apiget = '/api/v1/data/projectcall/?format=json&project=' + projectid;
                            debugger;
                            $http.get(apiget).then(function successCallback(response) {

                                debugger;
                            });
                        /*    var apiget = '/api/v1/data/projectorganization/?format=json&call=' + projectid;

                             $http.get(apiget).then(function successCallback(response) {

                                debugger;

                            });*/

                    }
                }

        }]

    }
);
