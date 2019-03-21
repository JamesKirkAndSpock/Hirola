$('#quantity').change(function() {
    $.getJSON("/hot_deal_quantity_change", {qty: $('#quantity').val(), phone_model_item: $('#phone_item').val(), view: 'json'}, function(j) {
        $total = comma(j.total_cost)
        $('#price').html(j.currency + "  " + $total);
    });
});

function comma(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}