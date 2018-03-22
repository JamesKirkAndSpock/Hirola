function revealSearch(searchField){
    var searchField = document.getElementById(searchField);
    if (searchField.style.visibility === 'hidden') {
        searchField.style.visibility = 'visible';
    } else {
        searchField.style.visibility = 'hidden';
    }

}
