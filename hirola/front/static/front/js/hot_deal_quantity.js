$('#quantity').change(function() {
    $.getJSON("/hot_deal_quantity_change", {qty: $('#quantity').val(), phone_model_item: $('#phone_item').val(), view: 'json'}, function(j) {
    $('#price').html(j.currency + "  " + comma(j.total_cost));
    });
});