// $('select#color').on('change', function () {
//     var select = $('#quantityRow .dropdown-content');
//     select.empty();
//     var pk = this.value;
//     Object.keys(quantities).forEach(function (key) {
//         if(pk == quantities[key].color){
//         var quantity = quantities[key].quantity;
//             for(var i=1; i<=quantity; i++){
//                 var li = $('<li></li>');
//                 li.attr('value', i);
//                 li.html(i);
//                 select.append(li);
//             }
//         }
//     });
// });

$('.materialSelect').on('change', function () {
    // $('#quantity).not(:first)').empty();
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