function w3_open() {
    document.getElementById("mySidebar").style.display = "block";
    document.getElementById("myOverlay").style.display = "block";
}

function w3_close() {
    document.getElementById("mySidebar").style.display = "none";
    document.getElementById("myOverlay").style.display = "none";
}

// Change style of top container on scroll

function openTab(evt, tabName) {

}

function myAccFunc() {
    var x = document.getElementById("demoAcc");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
        x.previousElementSibling.className += "  w3-theme-d3";
    } else {
        x.className = x.className.replace(" w3-show", "");
        x.previousElementSibling.className =
            x.previousElementSibling.className.replace("  w3-theme-d3", "");
    }
}

function metricShow(where) {

    var x = document.getElementById(where);
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
        x.previousElementSibling.className += "  w3-theme-d3";
    } else {
        x.className = x.className.replace(" w3-show", "");
        x.previousElementSibling.className =
            x.previousElementSibling.className.replace("  w3-theme-d3", "");
    }
}

function addData(where) {
    if (where == 'orgs') {
        var dom_el = document.querySelector('[ng-controller="HandleSearchEvents"]');
        var ng_el = angular.element(dom_el);
        var ng_el_scope = ng_el.scope();
        var Orgs = ng_el_scope["Orgs"];
        try {
            var x = document.getElementsByName("busquedaorg");
            if (Orgs.length > 0) {
                for (var i = 0; i < x.length; i++) {

                    x[i].innerText = Orgs[i]["nombre"];
                    x[i].style.fontSize = "smaller";
                    x[i].href = "/www/#!/metric" + Orgs[i].id;
                }
            }
        } catch (err) {
            ;
        }
    } else if (where == 'proy') {
        var dom_el = document.querySelector('[ng-controller="HandleSearchEvents"]');
        var ng_el = angular.element(dom_el);
        var ng_el_scope = ng_el.scope();
        var Proyectos = ng_el_scope["Proyectos"];
        try {
            var x = document.getElementsByName("busquedaproy");
            if (Proyectos.length > 0) {
                for (var i = 0; i < x.length; i++) {

                    x[i].innerText = Proyectos[i]["tituloProyecto"];
                    x[i].style.fontSize = "smaller";
                    x[i].href = "/www/#!/p" + Proyectos[i].id;
                }
            }
        } catch (err) {
            ;
        }
    }
}


