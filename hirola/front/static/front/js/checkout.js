$(document).ready(function(){
    $(document).ready(function(){
    $('select').formSelect();
      });
    $.getJSON("/country_codes", {id: $('#id_country_code').val(), view: 'json'}, function(j) {
        var options = '<option value="">--------&nbsp;</option>';
        for (var i in j["data"]) {
        if ( j["users_country_code"] == i ) {
            options += '<option value="' + i + '" selected>' + j["data"][i] + '</option>';
        }
        else {
        options += '<option value="' + i + '">' + j["data"][i] + '</option>';
        }
        }
        $('#countryCode').html(options);
    })

    $('#shippingMethod').click(function(){
        var radioValue = $("input[name='pickup']:checked").attr('id');
        if(radioValue === 'delivery'){
            $('.payment').css('display', 'block');
            $('#pickupOption').val("1");
            $('#tel').attr('required', true)
            $('#town').attr('required', true)
        }else {
            $('.payment').css('display', 'none');
            $('#pickupOption').val("0");
            $('#tel').attr('required', false)
            $('#town').attr('required', false)
        }
    });
});

