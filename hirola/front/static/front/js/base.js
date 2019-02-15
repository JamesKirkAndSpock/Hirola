var wordsToSplit = $('#dropdown').html();
var array = wordsToSplit.split(' ')
var string = array[0] + ' ..'
var renameField = function(){
    var widthOutput = window.innerWidth;
    if (widthOutput <= 768){
        $("[id='Home Tech']").html('H-Tech');
        $('#dropdown').html(string);
    }
    else {
        $("[id='Home Tech']").html('Home Tech');
        $('#dropdown').html(wordsToSplit);
    }
};
function resize() {
    renameField();
}
window.onresize = resize;
