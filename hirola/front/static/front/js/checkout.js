$(document).ready(function(){
    $('#shippingMethod').click(function(){
        var radioValue = $("input[name='group1']:checked").attr('id');
        if(radioValue === 'delivery'){
            $('.payment').css('display', 'block');
        }else {
            $('.payment').css('display', 'none');
        }
    });
});