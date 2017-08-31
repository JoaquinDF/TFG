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
  var i, x, tablinks;
  x = document.getElementsByClassName("tab");

  for (i = 0; i < x.length; i++) {
     x[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < x.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" w3-theme-d1", "");
  }
  document.getElementById(tabName).style.display = "block";

  if(evt!=null)evt.currentTarget.className += " w3-theme-d1";


}


