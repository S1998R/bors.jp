function agree_confirm() {
    if(agree_1.checked && agree_2.checked){
        document.getElementById("register_button_div").classList.add("z_index");
    }else {
        document.getElementById("register_button_div").classList.remove("z_index");
    }
}
