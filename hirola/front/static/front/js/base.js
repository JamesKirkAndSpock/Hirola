$(document).ready(function () {
    var trig = 1;
    //fix for chrome
    $("#search").addClass('searchbarfix');


    //animate searchbar width increase to  +150%
    $('#search').click(function (e) {
        //handle other nav elements visibility here to avoid push down
        $('.search-hide').addClass('hide');
        if (trig == 1) {
            $('#navfix2').animate({
                width: '+=150',
                marginRight: 0
            }, 400);

            trig++;
        }

    });

    // if user leaves the form the width will go back to original state

    $("#search").focusout(function () {

        $('#navfix2').animate({
            width: '-=150'
        }, 400);
        trig = trig - 1;
        //handle other nav elements visibility first to avoid push down
        $('.search-hide').removeClass('hide');

    });

});
