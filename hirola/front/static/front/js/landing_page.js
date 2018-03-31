
$(document).ready(function (){
    $("#search-button").click(function() {
        var choice = 0;
        if ($("#search-input").attr("type") === "search" && $("#search-input").attr("value") === "" ){
            choice = 0
        }
        
        if ($("#search-input").attr("type") === "hidden" && $("#search-input").attr("value") === "" ){
            choice = 1
        }
        switch(choice) {
            case 0:
                $("#search-input").attr("type", "hidden");
                break;
            case 1:
                $("#search-input").attr("type", "search");
                break;
        }
        return false;
    });
});

// LinkImageControls
function currentPhoneCategory(n) {
    showPhoneCategory(navbarIndex = n);
  }
  
  function showPhoneCategory(n) {
    // create a variable i
    var i;
    // get all the slides for images
    var navbarCategories = document.getElementsByClassName("nav-item");
    if (n > navbarCategories.length) {navbarIndex = 1} 
    if (n < 1) {navbarIndex = navbarCategories.length}
    for (i = 0; i < navbarCategories.length; i++) {
      navbarCategories[i].className = "nav-item ml-5 mr-5";
    }
    navbarCategories[navbarIndex-1].className = "nav-item ml-5 mr-5 active"; 
  }
var navbarIndex = 0;