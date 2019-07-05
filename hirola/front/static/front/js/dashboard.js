// toggle input divs
function editName(hiddenInput, visibleInput){
    var input = document.getElementById(hiddenInput);
    var output = document.getElementById(visibleInput);
    if (!input.style.display || input.style.display == 'none'){
        input.style.display = 'block';
        output.style.display = 'none';
    }else {
        input.style.display = 'none';
        output.style.display = 'block';
    }
}

var detailsLink = document.getElementById('details-link');
var detailsRow = document.getElementById('details');

$(document).ready(countryCodeSelector);
function countryCodeSelector() {
    $.getJSON("/country_codes", {id: $('#id_country_code').val(), view: 'json'}, function(j) {
        var options = '<option value="">--------&nbsp;</option>';
        for (var i in j["data"]) {
          if ( j["users_country_code"] == i ) {
            options += '<option value="' + i + '" selected>' + j["data"][i] + '</option>';
          }
          else {
          options += '<option value="' + i + '">' + j["data"][i] + '</option>';
          }
        }
    })
}

// When the user clicks on <div>, open the popup
function openPopup() {
  var popup = document.getElementById("inactiveEmailPopup");
  popup.classList.toggle("show");
}

function openDisplay(value) {
    var x = document.getElementById("details-"+value);
    switch (x.style.display) {
        case "":
        x.style.display = "block";
          break;
        case "none":
        x.style.display = "block";
          break;
        case "block":
        x.style.display = "none";
          break;
      }
  }


$(document).ready(function () {
    var sPath = window.location.pathname;
    var sPage = sPath.substring(sPath.lastIndexOf('/') + 1);
    success_messages.forEach(function (message) {
        if (sPage == 'dashboard'){
        M.toast({
            html: message,
            classes: "green"
        });
        }
    });
});

$(document).ready(function () {
  // activateTimer();
  getOrdersDiv();
});

function getOrdersDiv(){
  var divs = $('.count-down');
  for (var i=0; i<divs.length; i++){
    var $date = $(divs[i]).find('#purchaseDate').html();
    console.log($date);
    var $timeLeftdiv = $(divs[i]).find('#timeLeft');
    var $btn = $(divs[i]).find('#cancelOrderBtn');
    activateTimer($date, $timeLeftdiv, $btn);
  }
}

function activateTimer(date, timeLeftdiv, btn){
  var dateParts = date.split(" ");
  var month, day, year, time, noonPeriod;
  month = dateParts[0];
  day = dateParts[1];
  year = dateParts[2];
  time = dateParts[3];
  noonPeriod =dateParts[4];
  time = time + ':' + '00';
  var initialDate = new Date(month+ ' '+ day+ ','+ ' ' + year+ ' ' + time);
  var countDownDate = new Date(initialDate.getTime() + 60 * 60 * 48 * 1000);
  countDownDate = countDownDate.getTime();

  // Update the count down every 1 second
  var x = setInterval(function() {
    var now = new Date().getTime();
    var distance = countDownDate - now;
    seconds = Math.floor((distance % (1000 * 60)) / 1000);
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    $(timeLeftdiv).html(days + "d " + hours + "h " + minutes + "m " + seconds + "s ");

    if (distance < 0) {
      clearInterval(x);
      $(timeLeftdiv).html("EXPIRED");
      $(btn).attr("disabled", true);
      $.ajax({
        type: 'PUT',
        dataType: 'json',
        url: "/disable_cancel_order",
        data: {"order_id": $('#orderPk').val()}
    });
    }
  }, 1000);
}
