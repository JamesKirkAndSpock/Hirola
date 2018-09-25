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
var statusLink = document.getElementById('status-link');
var statusRow = document.getElementById('status');

detailsLink.addEventListener('click',() => {
    if(!detailsRow.style.display || detailsRow.style.display == 'none'){
        if (statusRow.style.display === 'block') {
            statusRow.style.display = 'none';
        }
        detailsRow.style.display = 'block';
    }else{
        detailsRow.style.display = 'none';
    }
});

statusLink.addEventListener('click', () => {
    if (!statusRow.style.display || statusRow.style.display === 'none'){
        if (detailsRow.style.display === 'block'){
            detailsRow.style.display = 'none';
        }
        statusRow.style.display = 'block';
    }else {
        statusRow.style.display = 'none';
    }
});

var currentDate = document.getElementById('current-date');
var now = new Date();
currentDate.innerHTML = now;