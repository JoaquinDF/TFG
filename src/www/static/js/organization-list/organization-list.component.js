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
                self.currentpageorganizations = 0;
                self.pagecounterorganizations;

                self.nextorganization = function () {
                    if (self.organizationsnext) {
                        $http.get(self.organizationsnext).then(function (responseorganizations) {

                            if (responseorganizations.data) {

                                self.organizations = responseorganizations.data.results;
                                self.organizationsnext = responseorganizations.data.next;
                                self.organizationsprev = responseorganizations.data.previous;
                                self.currentpageorganizations += 1;
                                self.pagecounterorganizations=null;
                            }
                        });
                    }
                }
                self.prevorganization = function () {
                    if (self.currentpageorganizations > 0) {
                        $http.get(self.organizationsprev).then(function (responseorganizations) {
                            if (responseorganizations.data) {
                                self.organizations = responseorganizations.data.results;
                                self.organizationsnext = responseorganizations.data.next;
                                self.organizationsprev = responseorganizations.data.previous;
                                self.currentpageorganizations -= 1;
                                self.pagecounterorganizations=null;

                            }
                        });
                    }
                }


                self.changepage = function (page) {
                    if (!isNaN(page) && page && page <= self.countorganizations) {
                          self.currentpageorganizations = parseInt(page);
                        page *= 10;
                        var http = "/api/v1/extract/data/?collection=data.organizations&limit=10&offset=" + page;

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
