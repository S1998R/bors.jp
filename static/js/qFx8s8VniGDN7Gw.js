


var bg = $('#loader-bg'),
    loader = $('#loader');

    bg.removeClass('is-hide');
    loader.removeClass('is-hide');

    $(window).on('load', stopload);

    setTimeout('stopload()',1000);

    function stopload(){
        bg.delay(900).fadeOut(800);
        loader.delay(900).fadeOut(300);
    }

    window.onload = function(){
       document.getElementById("condition_all_category").classList.add("condition_selected");
       document.getElementById("condition_all").classList.add("condition_selected");
    }

    function textbook_selected(){
       document.getElementById("condition_textbook").classList.add("condition_selected");
       document.getElementById("condition_others").classList.remove("condition_selected");
       document.getElementById("condition_all_category").classList.remove("condition_selected");

       var sell = document.getElementById('condition_sell');
       var sell_result = sell.classList.contains('condition_selected');

       if (sell_result) {
       let elements = document.getElementsByClassName("sell_textbook");
       Array.prototype.forEach.call(elements, function (element) {
       element.classList.remove("merchandise_none");
       });
       let elements_2 = document.getElementsByClassName("sold_textbook");
       Array.prototype.forEach.call(elements_2, function (element) {
       element.classList.add("merchandise_none");
       });
       }else{
       let elements_3 = document.getElementsByClassName("sell_textbook");
       Array.prototype.forEach.call(elements_3, function (element) {
       element.classList.remove("merchandise_none");
       });
       let elements_4 = document.getElementsByClassName("sold_textbook");
       Array.prototype.forEach.call(elements_4, function (element) {
       element.classList.remove("merchandise_none");
       });
       }

       let elements_5 = document.getElementsByClassName("sell_other");
       Array.prototype.forEach.call(elements_5, function (element) {
       element.classList.add("merchandise_none");
       });

       let elements_6 = document.getElementsByClassName("sold_other");
       Array.prototype.forEach.call(elements_6, function (element) {
       element.classList.add("merchandise_none");
       });

    }

    function others_selected(){
       document.getElementById("condition_others").classList.add("condition_selected");
       document.getElementById("condition_textbook").classList.remove("condition_selected");
       document.getElementById("condition_all_category").classList.remove("condition_selected");

       var sell = document.getElementById('condition_sell');
       var sell_result = sell.classList.contains('condition_selected');

       if (sell_result) {
       let elements = document.getElementsByClassName("sell_other");
       Array.prototype.forEach.call(elements, function (element) {
       element.classList.remove("merchandise_none");
       });
       let elements_2 = document.getElementsByClassName("sold_other");
       Array.prototype.forEach.call(elements_2, function (element) {
       element.classList.add("merchandise_none");
       });
       }else{
       let elements_3 = document.getElementsByClassName("sell_other");
       Array.prototype.forEach.call(elements_3, function (element) {
       element.classList.remove("merchandise_none");
       });
       let elements_4 = document.getElementsByClassName("sold_other");
       Array.prototype.forEach.call(elements_4, function (element) {
       element.classList.remove("merchandise_none");
       });
       }

       let elements_5 = document.getElementsByClassName("sell_textbook");
       Array.prototype.forEach.call(elements_5, function (element) {
       element.classList.add("merchandise_none");
       });

       let elements_6 = document.getElementsByClassName("sold_textbook");
       Array.prototype.forEach.call(elements_6, function (element) {
       element.classList.add("merchandise_none");
       });
    }

    function all_category_selected(){
       document.getElementById("condition_all_category").classList.add("condition_selected");
       document.getElementById("condition_others").classList.remove("condition_selected");
       document.getElementById("condition_textbook").classList.remove("condition_selected");

       var sell = document.getElementById('condition_sell');
       var sell_result = sell.classList.contains('condition_selected');

       if (sell_result) {
       let elements = document.getElementsByClassName("sell_textbook");
       Array.prototype.forEach.call(elements, function (element) {
       element.classList.remove("merchandise_none");
       });
       let elements_2 = document.getElementsByClassName("sell_other");
       Array.prototype.forEach.call(elements_2, function (element) {
       element.classList.remove("merchandise_none");
       });
       let elements_3 = document.getElementsByClassName("sold_textbook");
       Array.prototype.forEach.call(elements_3, function (element) {
       element.classList.add("merchandise_none");
       });
       let elements_4 = document.getElementsByClassName("sold_other");
       Array.prototype.forEach.call(elements_4, function (element) {
       element.classList.add("merchandise_none");
       });
       }else{
       let elements_5 = document.getElementsByClassName("sell_textbook");
       Array.prototype.forEach.call(elements_5, function (element) {
       element.classList.remove("merchandise_none");
       });
       let elements_6 = document.getElementsByClassName("sell_other");
       Array.prototype.forEach.call(elements_6, function (element) {
       element.classList.remove("merchandise_none");
       });
       let elements_7 = document.getElementsByClassName("sold_textbook");
       Array.prototype.forEach.call(elements_7, function (element) {
       element.classList.remove("merchandise_none");
       });
       let elements_8 = document.getElementsByClassName("sold_other");
       Array.prototype.forEach.call(elements_8, function (element) {
       element.classList.remove("merchandise_none");
       });
       }
    }


    function sell_selected(){
       document.getElementById("condition_sell").classList.toggle("condition_selected");
       document.getElementById("condition_all").classList.remove("condition_selected");

       var all = document.getElementById('condition_all_category');
       var all_result = all.classList.contains('condition_selected');
       var textbook = document.getElementById('condition_textbook');
       var textbook_result = textbook.classList.contains('condition_selected');
       var other = document.getElementById('condition_others');
       var other_result = other.classList.contains('condition_selected');

       if (all_result) {
       let elements = document.getElementsByClassName("sell_textbook");
       Array.prototype.forEach.call(elements, function (element) {
       element.classList.remove("merchandise_none");
       });
       let elements_2 = document.getElementsByClassName("sell_other");
       Array.prototype.forEach.call(elements_2, function (element) {
       element.classList.remove("merchandise_none");
       });
       }else if (textbook_result){
       let elements_3 = document.getElementsByClassName("sell_textbook");
       Array.prototype.forEach.call(elements_3, function (element) {
       element.classList.remove("merchandise_none");
       });
       let elements_4 = document.getElementsByClassName("sell_other");
       Array.prototype.forEach.call(elements_4, function (element) {
       element.classList.add("merchandise_none");
       });
       }else{
       let elements_5 = document.getElementsByClassName("sell_textbook");
       Array.prototype.forEach.call(elements_5, function (element) {
       element.classList.add("merchandise_none");
       });
       let elements_6 = document.getElementsByClassName("sell_other");
       Array.prototype.forEach.call(elements_6, function (element) {
       element.classList.remove("merchandise_none");
       });
       }

       let elements_7 = document.getElementsByClassName("sold_textbook");
       Array.prototype.forEach.call(elements_7, function (element) {
       element.classList.add("merchandise_none");
       });
       let elements_8 = document.getElementsByClassName("sold_other");
       Array.prototype.forEach.call(elements_8, function (element) {
       element.classList.add("merchandise_none");
       });
    }


    function all_selected(){
       document.getElementById("condition_all").classList.add("condition_selected");
       document.getElementById("condition_sell").classList.remove("condition_selected");

       var all = document.getElementById('condition_all_category');
       var all_result = all.classList.contains('condition_selected');
       var textbook = document.getElementById('condition_textbook');
       var textbook_result = textbook.classList.contains('condition_selected');
       var other = document.getElementById('condition_others');
       var other_result = other.classList.contains('condition_selected');

       if (all_result) {
       let elements = document.getElementsByClassName("sell_textbook");
       Array.prototype.forEach.call(elements, function (element) {
       element.classList.remove("merchandise_none");
       });
       let elements_2 = document.getElementsByClassName("sell_other");
       Array.prototype.forEach.call(elements_2, function (element) {
       element.classList.remove("merchandise_none");
       });
       let elements_3 = document.getElementsByClassName("sold_textbook");
       Array.prototype.forEach.call(elements_3, function (element) {
       element.classList.remove("merchandise_none");
       });
       let elements_4 = document.getElementsByClassName("sold_other");
       Array.prototype.forEach.call(elements_4, function (element) {
       element.classList.remove("merchandise_none");
       });
       }else if (textbook_result){
       let elements_5 = document.getElementsByClassName("sell_textbook");
       Array.prototype.forEach.call(elements_5, function (element) {
       element.classList.remove("merchandise_none");
       });
       let elements_6 = document.getElementsByClassName("sell_other");
       Array.prototype.forEach.call(elements_6, function (element) {
       element.classList.add("merchandise_none");
       });
       let elements_7 = document.getElementsByClassName("sold_textbook");
       Array.prototype.forEach.call(elements_7, function (element) {
       element.classList.remove("merchandise_none");
       });
       let elements_8 = document.getElementsByClassName("sold_other");
       Array.prototype.forEach.call(elements_8, function (element) {
       element.classList.add("merchandise_none");
       });
       }else{
       let elements_9 = document.getElementsByClassName("sell_textbook");
       Array.prototype.forEach.call(elements_9, function (element) {
       element.classList.add("merchandise_none");
       });
       let elements_10 = document.getElementsByClassName("sell_other");
       Array.prototype.forEach.call(elements_10, function (element) {
       element.classList.remove("merchandise_none");
       });
       let elements_11 = document.getElementsByClassName("sold_textbook");
       Array.prototype.forEach.call(elements_11, function (element) {
       element.classList.add("merchandise_none");
       });
       let elements_12 = document.getElementsByClassName("sold_other");
       Array.prototype.forEach.call(elements_12, function (element) {
       element.classList.remove("merchandise_none");
       });
       }
    }