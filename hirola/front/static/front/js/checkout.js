$(document).ready(function(){
    $('#shippingMethod').click(function(){
        var radioValue = $("input[name='pickup']:checked").attr('id');
        if(radioValue === 'delivery'){
            changeBehavior("block", "1", true);
        }else {
            changeBehavior("none", "0", false);
        }
    });
});

function changeBehavior(displayValue, pickUpvalue, inputsValue){
    $('.payment').css('display', displayValue);
    $('#pickupOption').val(pickUpvalue);
    $('#tel').attr('required', inputsValue);
    $('#town').attr('required', inputsValue);
}