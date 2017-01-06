/* option one: use snippet editor */
function product_change(product){
    if (product != "") {
        openerp.jsonRpc("/product_snippet/product_change", "call", {
            'product': product
        }).done(function(data){
            $.each($(".product_snippet"), function() {
                var src = $(this).find(".img").attr("data-cke-saved-src");
                if(src != undefined && !src.match("^data:")) {
                    $(this).find(".img").attr({
                        "data-cke-saved-src": "data:image/png;base64," + data['image'],
                        "src": "data:image/png;base64," + data['image']
                    });
                    $(this).find("h2").html("<span>" + data['name'] + "</span>");
                    $(this).find("p").html("<span>" + data['description'] + "</span>");
                    return false;
                }
            });
        });
    }
}

function col_change(col) {
    $(".product_snippet").attr({
        "class": "product_snippet col-md-" + col +" mb16 mt16"
    });
}

/*
 * option two: use pure javascript
var current_element;

$(".product_snippet").click(function(e) {
    $('#product_selector').css({'display': 'unset', "top": e.pageY, "left": e.pageX});
    $('#col_selector').css({'display': 'unset', "top": e.pageY + 35, "left": e.pageX});
    current_element = $(this);
});

$(document).ready(function() {
    $("body").append("<select id='product_selector'></select><select id='col_selector'><option value='3' onclick='col_change(3)'>col-3</option><option value='4' onclick='col_change(4)'>col-4</option><option value='6' onclick='col_change(6)'>col-6</option><option value='12' onclick='col_change(12)'>col-12</option></select>");
    openerp.jsonRpc("/product_snippet/get_products", "call", {
    }).done(function(data){
        $('#product_selector').append($("<option>", {
            value: "",
            text: "-- Choose a product --"
        }));
        $.each(data, function( key, value ) {
            $('#product_selector').append($("<option>", {
                value: key,
                text: value,
                onclick: "product_change(" + key + ")"
            }));
        });
    });
});

function product_change(product_id){
    if (product_id != "") {
        openerp.jsonRpc("/product_snippet/product_change", "call", {
            'product': product_id
        }).done(function(data){
            current_element.find(".img").attr({
                "src": "data:image/png;base64," + data['image'],
            });
            current_element.find("h2").html("<span>" + data['name'] + "</span>");
            current_element.find("p").html("<span>" + data['description'] + "</span>");
        });
    }
}

function col_change(col) {
    current_element.attr({
        "class": "product_snippet col-md-" + col +" mb16 mt16"
    });
}
* */
