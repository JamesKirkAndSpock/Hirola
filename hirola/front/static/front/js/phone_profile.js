$(document).ready(function () {
    $('#lightSlider').lightSlider({
        gallery: true,
        item: 1,
        loop: true,
        thumbItem: 9,
        slideMargin: 0,
        enableDrag: false,
        currentPagerPosition: 'left',
        prevHtml: '<i class="fas fa-chevron-left fa-2x"></i>',
        nextHtml: '<i class="fas fa-chevron-right fa-2x"></i>'
    });
});

$("select[required]").css({display: "block", height: 0, padding: 0, width: 0, position: 'absolute'});

$(document).ready(function () {
    error_messages.forEach(function (message) {
        M.toast({
            html: message,
            classes: "red"
        });
       delete error_messages[message];
    });
});
