// initialize carousel
$(document).ready(function () {
    var elements = document.getElementsByClassName("carousel-item");
    $('.carousel').carousel();
    // set autoplay if images are more than one
    if (elements.length > 1)
        {
        $('.carousel.carousel-slider').carousel({ fullWidth: true }, setTimeout(autoplay, 4000));
        function autoplay() {
            $('.carousel').carousel('next');
            setTimeout(autoplay, 4000);
        }
        }
});

// initialize side nav
// $(".button-collapse").sideNav();

// initialize tabs
$(document).ready(function(){
    $('.tabs').tabs();
});

// initialize collapsible
$(document).ready(function(){
  $('.collapsible').collapsible();
});

// Reinitialize the labels on the page for dynamically adding inputs
$(document).ready(function () {
    M.updateTextFields();
});

// initialize the materialize select
 $(document).ready(function () {
     $('select').formSelect();
 });

// trigger modal
$(document).ready(function () {
    $('.modal').modal();
});

// trigger side-nav
$(document).ready(function(){
    $('.sidenav').sidenav({
        edge: 'right'
    });
});

// trigger dropdown
$(".dropdown-trigger").dropdown();

$(document).ready(function(){
    $('.tooltipped').tooltip();
  });
