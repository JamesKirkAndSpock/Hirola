$('#color_selector').change(function() {
    $.getJSON("/get_sizes", {id: $('#color_selector').val(), phone_model_id: $('#phone_model').val(), view: 'json'}, function(j) {

        var options = '<option value="' + j["phone_size_id"] + '" selected>' + j["phone_size"] + '</option>';
        for (var i in j.sizes) {
            options += '<option value="' + i + '">' + j.sizes[i] + '</option>';
        }
        $('select').formSelect();
        var instance = M.FormSelect.getInstance($("#storage"));
        $("#storage").html('');
        $("#storage").html(options);
        var quantity_options = '<option value=1 selected>1</option>';
        for (var i=2, k=2 ; i <= j.phone_quantity; i ++ , k++){
            quantity_options += '<option value=' + k + '>'+ i + '</option> ';
        }
        $("#quantity").html(quantity_options);
        $price = commaFunction(j.price);
        $('#price').html(j.currency + "  " + $price);
        $('select').formSelect();
        $('#main_image_data_thumb').attr("data-thumb", j["main_image"])
        $('#main_image_src').attr("src", j["main_image"]);
        var  feature_list = "";
        for( feature in j["features"]){
            feature_list += '<li>'+ j["features"][feature] + '</li>';
        }
        $('#phone_features').html(feature_list);
        var infos = "";
        for (i in j["infos"]){
            infos += '<div class="row detail">' + '<div class="col s6" id="title">' + i + '</div>' +
            '<div class="col s6">' + j["infos"][i] + '</div></div>'
        }
        $('#product_information').html(infos);
        $("#phone_item").val(j.phone);
    })
});

$('#storage').change(function() {
    $.getJSON("/size_change", {size_id: $('#storage').val(), phone_model_id: $('#phone_model').val(), view: 'json'}, function(j) {
        var quantity_options = '<option value=1 selected>1</option>';
        for (var i=2, k=2; i <= j.phone_quantity; i ++, k++ ){
            quantity_options += '<option value=' + k + '>'+ i + '</option> ';
        }
        $("#quantity").html(quantity_options);
        $('select').formSelect();
        $price = commaFunction(j.price);
        $('#price').html(j.currency + "  " + $price);
        $("#phone_item").val(j.phone);
    })
});

$('#quantity').change(function() {
    $.getJSON("/quantity_change", {color_id: $('#color_selector').val(), size_id: $('#storage').val(), qty: $('#quantity').val(), phone_model_id: $('#phone_model').val(), view: 'json'}, function(j) {
        $total = commaFunction(j.total_cost);
        $('#price').html(j.currency + "  " + $total);
    })
});
