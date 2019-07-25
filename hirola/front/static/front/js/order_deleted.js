$(document).ready(function(){
    $('#clientReasonForm').click(function(){
        var radioValue = $("input[name='group1']:checked").attr('id');
        if(radioValue === 'somethingElseRadio'){
            changeBehavior("block", '', true);
        }else if(radioValue === 'cheaperRadio'){
            changeBehavior("none", 'Found a cheaper item somewhere.', false);
        }else if(radioValue === 'expensiveRadio'){
            changeBehavior("none", 'Item was too expensive.', false);
        }else if(radioValue === 'uneededRadio'){
            changeBehavior("none", 'I don\'t need the item any more.', false);
        }
    });
});

function changeBehavior(displayValue, inputValue, required){
    $('#somethingElseInput').css('display', displayValue).attr('required', required);
    $('#hidden').val(inputValue);
}