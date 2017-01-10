/* option one: use snippet editor */
function product_change(product){
    if (product != "") {
        openerp.jsonRpc("/product_snippet/product_change", "call", {
            'product': product
        }).done(function(data){
            $.each($(".individual_product"), function() {
                var src = $(this).find(".img").attr("data-cke-saved-src");
                if(src != undefined && !src.match("^data:")) {
                    $(this).find(".img").attr({
                        "data-cke-saved-src": "data:image/png;base64," + data['image'],
                        "src": "data:image/png;base64," + data['image']
                    });
                    $(this).find("h3").html("<span>" + data['name'] + "</span>");
                    $(this).find(".o_footer").find("small").html("<span>" + data['description'] + "</span>");
                    return false;
                }
            });
        });
    }
}

function ind_col_change(col) {
    $(".individual_product").attr({
        "class": "individual_product col-md-" + col +" mb16 mt16"
    });
}

function get_products_by_category(categ_id){
    if (categ_id != "") {
        openerp.jsonRpc("/product_snippet/get_products_by_category", "call", {
            'categ_id': categ_id
        }).done(function(data){
            var counter = 1; // for some reason the first loop does not allowed to insert html
            $.each($(".products_by_category"), function() {
                if(counter == 2){
                    var product_content = "";
                    $.each(data, function(key, info) {
                        product_content += "<div class='pbc_outter'><div class='pbc_inner'><h3 class='text-center'>" + data[key]['name'] +"</h3><img src='data:image/png;base64," + data[key]['image'] + "' data-cke-saved-src='data:image/png;base64," + data[key]['image'] + "'/><p>" + data[key]['description'] + "</p></div></div>";
                    });
                    $(this).find(".products_by_category_content").html(product_content);
                    //~ $(this).find(".products_by_category_content").find(".pbc").attr({"class": "col-md-4"});
                }
                if(counter == 3){
                    return false;
                }
                counter ++;
            });
        });
    }
}

function pbc_col_change(col) {
    $(".pbc_outter").attr({
        "class": "pbc_outter col-md-" + col
    });
}



/*
 * option two: use pure javascript
var current_element;

$(".individual_product").click(function(e) {
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

function ind_col_change(col) {
    current_element.attr({
        "class": "individual_product col-md-" + col +" mb16 mt16"
    });
}
* */
