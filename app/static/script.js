function myFunction() {
      document.getElementById("myDropdown").classList.toggle("show");
  }

function roll() {
    window.location.replace('/');
  }

window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {

      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }

$(document).ready(function() {
  $(".dropdown").click(function(){
      $(".results-container").toggleClass("blur");
      console.log("Hola");
  });
});