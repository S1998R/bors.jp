function nidoosi_for_refund(form) {
    var image = document.getElementById("id_image").value;
    var cases = document.getElementById("cases").value;

    if(cases == 'はい'){
        if (!image){
            document.getElementById("image_none_error").classList.remove("none");
            return false;
        }
    }

    var elements = form.elements;
    for (var i = 0; i < elements.length; i++) {
    if (elements[i].type == 'submit') {
    elements[i].disabled = true;
    }
    }
    }