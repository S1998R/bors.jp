function nidoosi_sell_form(form) {
    var image = document.getElementById("id_image").value;

    if (!image){
        document.getElementById("image_none_error").classList.remove("none");
        return false;
    }

    var elements = form.elements;
    for (var i = 0; i < elements.length; i++) {
    if (elements[i].type == 'submit') {
    elements[i].disabled = true;
    }
    }
    }