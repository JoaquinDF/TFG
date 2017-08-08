'use strict';

// Register `countList` component, along with its associated controller and template!
angular.
  module('callList').
  component('callList', {

    templateUrl: '/static/templates/call-list.template.html',
    controller: ['$http', function CallsListController($http , $scope) {
      var self = this;
      $http.get('/api/v1/extract/data/?collection=data.calls&limit=10&offset=0').then(function(responsecalls) {

        self.calls = responsecalls.data.results;
        debugger;
        self.callsnext = responsecalls.data.next;
        self.callsprev = responsecalls.data.previous;
        self.countcalls = Math.floor((responsecalls.data.count)/10);
        self.currentpagecalls = 0;
        self.nextcall = function () {
            if(self.callsnext) {
                $http.get(self.callsnext).then(function (responsecalls) {

                    if (responsecalls.data) {

                       self.calls = responsecalls.data.results;
                      self.callsnext = responsecalls.data.next;
                      self.callsprev = responsecalls.data.previous;
                        self.currentpagecalls+=1;
                    }
                });
            }
        }
        self.prevcall = function () {
          if(self.currentpagecalls>0) {
                $http.get(self.callsprev).then(function (responsecalls) {
                    if (responsecalls.data) {
                      self.calls = responsecalls.data.results;
                      self.callsnext = responsecalls.data.next;
                      self.callsprev = responsecalls.data.previous;
                      self.currentpagecalls-=1;

                    }
                });
            }
        }


        self.changepage = function (page) {
            if(!isNaN(page) && page && page<self.countcalls) {
                page*=10;
                var http = "/api/v1/extract/data/?collection=data.calls&limit=10&offset=" + page;

                console.log(http);
                $http.get(http).then(function (responsecalls) {
                    if (responsecalls.data) {

                        self.calls = responsecalls.data.results;

                        self.callsnext = responsecalls.data.next;
                        self.callsprev = responsecalls.data.previous;
                        self.pagecalls = page;
                        self.currentpagecalls=parseInt(page);

                    }
                });
            }
        }

      });





    }]

  }

);
