
var renameField = function(){
    var widthOutput = window.innerWidth;
    if (widthOutput <= 768){
        $("[id='Home Tech']").html('H Tech');
    }
    else {
        $("[id='Home Tech']").html('Home Tech');
    }
};
function resize() {
    renameField();
}
window.onresize = resize;

