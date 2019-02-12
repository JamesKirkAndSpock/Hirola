$('#color').on('change', function () {
    $('#quantityRow option').not(':first').remove();
    var pk = this.value;
    Object.keys(quantities).forEach(function (key) {
        if (pk == quantities[key].secondary_details) {
            var phone_quantity= comma(quantities[key].price);
            var price = quantities[key].currency + ' ' + phone_quantity;
            var quantity = quantities[key].quantity;
            $('#price').html(price);
            $('#size').val(quantities[key].size);
            $('#cart_phone_price').val(quantities[key].price);
            for (var i = 0; i <= quantity; i++) {
                $('select').formSelect();
                var $newOpt = $("<option>").attr("value", (i+1)).text(i + 1);
                $("#quantity").append($newOpt);
            }
        }
    });
});

function comma(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}

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
