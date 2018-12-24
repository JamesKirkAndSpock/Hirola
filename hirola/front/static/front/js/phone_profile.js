$('.materialSelect').on('change', function () {
    $('#quantityRow option').not(':first').remove();
    var pk = this.value;
    Object.keys(quantities).forEach(function (key) {
        if (pk == quantities[key].color) {
            var quantity = quantities[key].quantity;
            for (var i = 0; i <= quantity; i++) {
                $('select').formSelect();
                var $newOpt = $("<option>").attr("value", i).text(i+1);
                $("#quantity").append($newOpt);
            }
        }
    });
});
