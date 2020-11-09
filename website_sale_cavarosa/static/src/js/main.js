$(document).ready(function() {
    $("#elder20").click(function(){
        //~ $.cookie("age", "elder20");
        document.cookie = "age=elder20";
    });
});

$(window).on('load',function(){
    if(!getCookie("age") || getCookie("age") != "elder20") {
        $('#limit_modal').modal('show');
    }
});

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
