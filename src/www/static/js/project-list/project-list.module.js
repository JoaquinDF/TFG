'use strict';

// Define the `projectList` module
var plist = angular.module('projectList', []);


plist
.filter('custom', function() {
  return function(input, search) {

    if (!input) return input;
    if (!search) return input;
    var expected = ('' + search).toLowerCase();
    var result = {};
    angular.forEach(input, function(value, key) {
      var actual = ('' + value).toLowerCase();
      if (actual.indexOf(expected) !== -1) {
        result[key] = value;
      }
    });
    ;
    console.log("FIN")
    debugger;
      return result;
  }
});
/*

plist.filter('byCategory', function () {
    return function (input, search) {
        debugger;
    if (!input) return input;
    if (!search) return input;

    var modelo,busqueda; //modelo= que propiedad busqueda= que es
    var result = {};


    search = search.toLowerCase();

        var splited = search.split(" ");
        if(splited.length>2)return result;

        modelo = splited[0];
        busqueda = splited[1];

        //
debugger;
        if(modelo.indexOf("proyect")!=-1 || modelo.indexOf("project")!=-1){
debugger;
            if(busqueda === null){
                result = input.tituloProyecto;
                return result;
            }else{
                if(input.indexOf(search)!=-1){
                    result = input;
                    return result;
                }else {
                    return result;
                }
            }
        }





    }

})*/