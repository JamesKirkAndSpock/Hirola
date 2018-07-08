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

$(".button-collapse").sideNav();
