$('.materialSelect').on('change', function () {
    $('#quantityRow option').not(':first').remove();
    var pk = this.value;
    Object.keys(quantities).forEach(function (key) {
        if (pk == quantities[key].color) {
            var quantity = quantities[key].quantity;
            for (var i = 0; i <= quantity; i++) {
                $('select').formSelect();
                var $newOpt = $("<option>").attr("value", i).text(i + 1);
                $("#quantity").append($newOpt);
            }
        }
    });
});

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
