$(document).ready(function () {
    messages.forEach(function (message) {
        if (message.tag == 'error'){
            M.toast({
                html: message.message,
                classes: "red",
                displayLength: 6000
            });
        delete messages[message];
        }
        else if(message.tag == 'success'){
            M.toast({
                html: message.message,
                classes: "green"
            });
        delete messages[message];
        }
    });
});