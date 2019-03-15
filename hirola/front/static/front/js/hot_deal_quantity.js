$('#quantity').change(function() {
    $.getJSON("/hot_deal_quantity_change", {qty: $('#quantity').val(), phone_model_item: $('#phone_model_item').text(), view: 'json'}, function(j) {
    $('#price').html(j.currency + "  " + j.total_cost);
    });
});