// initialize carousel
$(document).ready(function () {
    $('.carousel').carousel();
});

// set autoplay
$('.carousel.carousel-slider').carousel({ fullWidth: true }, setTimeout(autoplay, 3000));
function autoplay() {
    $('.carousel').carousel('next');
    setTimeout(autoplay, 3000);
}
$(".button-collapse").sideNav();