var slideIndex = 1;
showSlides(slideIndex);

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  // create a variable i
  var i;
  // get all the slides for images
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dots");
  
  if (n > slides.length) {slideIndex = 1} 
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
      dots[i].className = "dots ml-3"
  }
  slides[slideIndex-1].style.display = "block"; 
  dots[slideIndex-1].className += " active";
}
var slideIndex = 0;
carousel();

function carousel() {
var i;
var x = document.getElementsByClassName("mySlides");
var y = document.getElementsByClassName("dots");
for (i = 0; i < x.length; i++) {
x[i].style.display = "none";
y[i].className = "dots ml-3"
}
slideIndex++;
if (slideIndex > x.length) {slideIndex = 1} 
x[slideIndex-1].style.display = "block";
y[slideIndex-1].className = "dots ml-3 active"
setTimeout(carousel, 2000); // Change image every 2 seconds
}


