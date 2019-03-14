$('#quantity').change(function() {
    $.getJSON("/hot_deal_quantity_change", {qty: $('#quantity').val(), phone_model_list_id: $('#phone_model_list_id').text(), view: 'json'}, function(j) {
    $('#price').html(j.currency + "  " + j.total_cost);
    });
});