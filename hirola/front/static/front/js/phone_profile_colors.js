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
        $('#price').html(j.currency + "  " + comma(j.price));
        $('select').formSelect();
        $('#main_image_data_thumb').attr("data-thumb", j["main_image"])
        $('#main_image_src').attr("src", j["main_image"]);
        var  feature_list = "<h6><b>Key Features</b></h6>";
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
        $(document).ready(function () {
            var profileImg = $('.profile-img');
            var lightSlider = $('<ul/>').attr('id', 'lightSlider');
            var mainImg = $('<li/>').attr('id', 'main_image_data_thumb');
            mainImg.attr("data-thumb", j.main_image);
            var mainImgSrc = $('<img/>').attr('id', 'main_image_src');
            mainImgSrc.attr({"src": j.main_image, 'height':150, 'width': 80});
            mainImg.append(mainImgSrc);
            lightSlider.append(mainImg);
            for (var img in j.images){
                var thumbLi = $('<li/>').attr('data-thumb', j.images[img]);
                thumbLi.addClass('center scroll-images');
                var thumbImg = $('<img/>').attr({'id': 'main_image_src', 'height':150, 'width': 80});
                thumbImg.attr("src", j.images[img]);
                thumbLi.append(thumbImg);
                lightSlider.append(thumbLi);
            }
            profileImg.html(lightSlider);
            lightSlider.lightSlider({
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
    })
});

$('#storage').change(function() {
    $("#phone_size").val($('#storage').val());

    $.getJSON("/size_change", {size_id: $('#storage').val(), phone_model_id: $('#phone_model').val(), view: 'json'}, function(j) {
        var quantity_options = '<option value=1 selected>1</option>';
        for (var i=2, k=2; i <= j.phone_quantity; i ++, k++ ){
            quantity_options += '<option value=' + k + '>'+ i + '</option> ';
        }
        $("#quantity").html(quantity_options);
        $('select').formSelect();
        $('#price').html(j.currency + "  " + comma(j.price));
        $("#phone_item").val(j.phone);
        console.log(j);
    })
});

$('#quantity').change(function() {
    $.getJSON("/quantity_change", {color_id: $('#color_selector').val(), size_id: $('#storage').val(), qty: $('#quantity').val(), phone_model_id: $('#phone_model').val(), view: 'json'}, function(j) {
    $('#price').html(j.currency + "  " + comma(j.total_cost));
    })
});

$('add-to-cart-button').click(function(){
    $('add-to-cart-button2').attr('name', '');
});