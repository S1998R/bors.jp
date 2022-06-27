$(document).ready(function(){
        var param = location.search;
        if (param=='?status=success') {
            document.getElementById("base_message_div").innerHTML = "<p><i class='fas fa-exclamation-circle'></i>出品が完了しました。</p>";
        }
    });


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


