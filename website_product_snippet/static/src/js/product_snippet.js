function product_change(product){
    if (product != "") {
        openerp.jsonRpc("/product_snippet/product_change", "call", {
            'product': product
        }).done(function(data){
            $(".product_snippet").find("#ps_img").attr({
                "id": "ps_img_product_" + data['id'],
                "data-cke-saved-src": "data:image/png;base64," + data['image'],
                "src": "data:image/png;base64," + data['image'],
            });
            $(".product_snippet").find("#ps_name").html("<span>" + data['name'] + "</span>");
            $(".product_snippet").find("#ps_name").attr({
                "id": "ps_name_product_" + data['id'],
            });
            $(".product_snippet").find("#ps_desc").html("<span>" + data['description'] + "</span>");
            $(".product_snippet").find("#ps_desc").attr({
                "id": "ps_desc_product_" + data['id'],
            });
        });
    }
}

function col_change(col) {
    $(".product_snippet").attr({
        "class": "product_snippet col-md-" + col +" mb16 mt16"
    });
}
