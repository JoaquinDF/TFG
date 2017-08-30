'use strict';

// Register `countList` component, along with its associated controller and template!
angular.module('searchList').component('searchList', {

        templateUrl: '/static/templates/search-list.template.html',
        controller: ['$http', function CallsListController($http, $scope) {
            var self = this;
              var x = document.URL;
              var projectid,organizationid;
              var regex = new RegExp('\/(p|o|c)[0-9a-zA-Z]*');
              var tipo = regex.exec(x);
              self.textsearch;
              self.selectsearch;

                if(tipo!=null) {
                    switch (tipo[1]) {
                        case 'p':
                            projectid = (tipo[0].split('/p'))[1];
                             var apiget = '/api/v1/data/project/?format=json&id=' + projectid;

                             $http.get(apiget).then(function successCallback(response) {
                                self.Proyecto=response.data.results;

                            });



                            var apiget = '/api/v1/data/projectcall/?format=json&project=' + projectid;
                            $http.get(apiget).then(function successCallback(response) {

                               var callidarray = response.data.results;
                               callidarray.forEach(function(id) {


                                            var apiget = '/api/v1/data/call/?format=json&id=' + id.convocatoria;
                                            $http.get(apiget).then(function successCallback(response) {
                                                self.Calls = [];
                                                self.Calls.push(response.data.results)
                                            });

                                });
                            });
                             var apiget = '/api/v1/data/projectorganization/?format=json&project=' + projectid;
                             debugger;
                            $http.get(apiget).then(function successCallback(response) {

                               var orgidarray = response.data.results;
                               orgidarray.forEach(function(id) {


                                            var apiget = '/api/v1/data/organization/?format=json&id=' + id.organizacion;
                                            $http.get(apiget).then(function successCallback(response) {
                                                self.Orgs = [];
                                                self.Orgs.push(response.data.results)

                                                debugger;
                                            });

                                });
                            });






                    }
                }

                self.search = function () {
                      var apiget = '/api/v1/data/' + self.selectsearch + '/?format=json&id=' + id.organizacion;
                    debugger;
                }

        }]

    }
);
