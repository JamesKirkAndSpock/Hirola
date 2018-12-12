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

detailsLink.addEventListener('click',() => {
    if(!detailsRow.style.display || detailsRow.style.display == 'none'){
        detailsRow.style.display = 'block';
    }else{
        detailsRow.style.display = 'none';
    }
});


var currentDate = document.getElementById('current-date');
var now = new Date();
currentDate.innerHTML = now;

$(document).ready(areaCodeSelector);
function areaCodeSelector() {
    $.getJSON("/area_codes", {id: $('#id_area_code').val(), view: 'json'}, function(j) {
        var options = '<option value="">--------&nbsp;</option>';
        for (var i in j["data"]) {
          if ( j["users_area_code"] == i ) {
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
