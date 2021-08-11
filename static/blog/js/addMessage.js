var addMessage = function (type, message) {
    $("#message_content").html("");
    $("#message_content").removeClass("message_success");
    $("#message_content").removeClass("message_error");
    if (message != null && message != '') {
        if (type == 'success') {
            $("#message_content").addClass("message_success");
        } else {
            $("#message_content").addClass("message_error");
        }
        $("#message_content").html(message);
        $("#message_info").fadeIn();
        setTimeout(function () {
            $("#message_info").fadeOut();
        }, 2500);
    }
};
