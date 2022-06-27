function nidoosi_for_talk_room(form) {
    var image = document.getElementById("talk_image").value;
    var comment = document.getElementById("id_comment").value;

    if(comment == false){
        if (!image){
            document.getElementById("talk_none_error").classList.remove("none");
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