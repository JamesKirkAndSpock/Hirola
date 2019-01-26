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
    console.log(sPage);
    success_messages.forEach(message => {
        if (sPage == 'dashboard'){
        M.toast({
            html: message,
            classes: "green"
        });
        }
    });
});
});
