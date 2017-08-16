'use strict';

// Register `projectList` component, along with its associated controller and template!
angular.module('organizationList').component('organizationList', {

        templateUrl: '/static/templates/organization-list.template.html',
        controller: ['$http', function OrganizationListController($http, $scope) {
            var self = this;
            $http.get('/api/v1/extract/data/?collection=data.organizations&limit=10&offset=0').then(function (responseorganizations) {

                self.organizations = responseorganizations.data.results;
                self.organizationsnext = responseorganizations.data.next;
                self.organizationsprev = responseorganizations.data.previous;
                self.countorganizations = Math.floor((responseorganizations.data.count) / 10);
                self.pagecounterorganizations;
                self.currentpage = 0;
                self.nextorganization = function () {

                    if (self.organizationsnext) {
                        $http.get(self.organizationsnext).then(function (responseorganizations) {

                            if (responseorganizations.data) {

                                self.organizations = responseorganizations.data.results;
                                self.organizationsnext = responseorganizations.data.next;
                                self.organizationsprev = responseorganizations.data.previous;
                                self.currentpage += 1;
                                  self.pagecounterorganizations=null;
                            }
                        });
                    }
                }
                self.prevorganization = function () {
                    if (self.currentpage > 0) {
                        $http.get(self.organizationsprev).then(function (responseorganizations) {
                            if (responseorganizations.data) {
                                self.organizations = responseorganizations.data.results;
                                self.organizationssnext = responseorganizations.data.next;
                                self.organizationssprev = responseorganizations.data.previous;
                                self.currentpage -= 1;
                                  self.pagecounterorganizations=null;

                            }
                        });
                    }
                }


                self.changepage = function (page) {
                    if (!isNaN(page) && page && page < self.countorganizations) {
                         self.currentpage = parseInt(page);
                        page *= 10;
                        var http = "/api/v1/extract/data/?collection=data.organizations&limit=10&offset=" + page;

                        console.log(http);
                        $http.get(http).then(function (responseorganizations) {
                            if (responseorganizations.data) {

                                self.organizations = responseorganizations.data.results;
                                self.organizationsnext = responseorganizations.data.next;
                                self.organizationsprev = responseorganizations.data.previous;


                            }
                        });
                    }
                }

            });


        }]

    }
);
