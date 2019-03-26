var $shipping = document.getElementById('shippingMethod');
// console.log($shipping);
// for (var i = 0; i < $shipping.length; i++){
//     if ($shipping[i].checked == true){
//         console.log($shipping[i]);
//     }
// }
$(document).ready(function(){
    $('#shippingMethod').click(function(){
        var radioValue = $("input[name='group1']:checked").attr('id');
        if(radioValue === 'delivery'){
            $('.payment').css('display', 'block')
        }else {
            $('.payment').css('display', 'none')
        }
    });

});