/**
 * Created by bisitemini on 17/8/17.
 */
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
function metricShow() {


    var x = document.getElementById("demoMetric");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
        x.previousElementSibling.className += "  w3-theme-d3";
    } else {
        x.className = x.className.replace(" w3-show", "");
        x.previousElementSibling.className =
            x.previousElementSibling.className.replace("  w3-theme-d3", "");
    }
}


