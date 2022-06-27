     function click_side_none(){
       document.getElementById("nav-content").classList.remove("transform_none_js");
       document.getElementById("bg").classList.remove("bg_js");
       document.getElementById("nth-of-type1").classList.remove("nth-of-type1_js");
       document.getElementById("nth-of-type2").classList.remove("nth-of-type2_js");
       document.getElementById("nth-of-type3").classList.remove("nth-of-type3_js");
       var ele = document.getElementsByClassName("image_div");
       for(var i = 0; i < ele.length; i++){
        ele[i].classList.remove("z-index");
    }
    }


    function click_burger(){
       document.getElementById("nav-content").classList.toggle("transform_none_js");
       document.getElementById("bg").classList.toggle("bg_js");
       document.getElementById("nth-of-type1").classList.toggle("nth-of-type1_js");
       document.getElementById("nth-of-type2").classList.toggle("nth-of-type2_js");
       document.getElementById("nth-of-type3").classList.toggle("nth-of-type3_js");
       var ele = document.getElementsByClassName("image_div");
       for(var i = 0; i < ele.length; i++){
        ele[i].classList.add("z-index");
    }
    }
