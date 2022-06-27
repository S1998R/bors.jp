function stop_check(){

	if(window.confirm('本当に出品を停止しますか？')){

		return true;

	}
	else{

		return false;

	}

}



function answer_edit(btn){
    var answer = btn.previousElementSibling.textContent;
    var answer_form_div = btn.nextElementSibling;
    var answer_form = answer_form_div.firstElementChild;
    var answer_form_and_button = answer_form.children[2];
    var answer_textarea = answer_form_and_button.firstElementChild;

    answer_textarea.value = answer;
    answer_form_div.classList.toggle("none");
}



$(function(){
    $('#subImg img').on('click',function(){

        img = $(this).attr('src');
        $('#subImg img').removeClass('focus_img');
        $('#subImg_2 img').removeClass('focus_img');
        $(this).addClass('focus_img');

        $('#subImg li').removeClass('current');
        $(this).parent().addClass('current');

        if ($('#mainImg img').length==1){
        $('#mainImg img').fadeOut(100, function() {
            $('#mainImg img').attr('src', img).on('load', function() {
                 $(this).fadeIn();
            })
       })
       }else {
        $('#mainImg').prepend('<img>');
        $('#mainImg img').attr('src', img).on('load', function() {
                 $(this).fadeIn();
            })
       }

    });
});


$(function(){
    $('#subImg_2 img').on('click',function(){

        img = $(this).attr('src');
        $('#subImg img').removeClass('focus_img');
        $('#subImg_2 img').removeClass('focus_img');
        $(this).addClass('focus_img');

        $('#subImg_2 li').removeClass('current');
        $(this).parent().addClass('current');

        if ($('#mainImg img').length==1){
        $('#mainImg img').fadeOut(100, function() {
            $('#mainImg img').attr('src', img).on('load', function() {
                 $(this).fadeIn();
            })
       })
       }else {
        $('#mainImg').prepend('<img>');
        $('#mainImg img').attr('src', img).on('load', function() {
                 $(this).fadeIn();
            })
       }

    });
});



$(function(){
    $('#subImg_subImg_in_explanation img').on('click',function(){

        img = $(this).attr('src');
        $('#subImg_subImg_in_explanation img').removeClass('focus_img');
        $('#subImg_2_subImg_in_explanation img').removeClass('focus_img');
        $(this).addClass('focus_img');

        $('#subImg li').removeClass('current');
        $(this).parent().addClass('current');

        if ($('#mainImg img').length==1){
        $('#mainImg img').fadeOut(100, function() {
            $('#mainImg img').attr('src', img).on('load', function() {
                 $(this).fadeIn();
            })
       })
       }else {
        $('#mainImg').prepend('<img>');
        $('#mainImg img').attr('src', img).on('load', function() {
                 $(this).fadeIn();
            })
       }
    });
});


$(function(){
    $('#subImg_2_subImg_in_explanation img').on('click',function(){

        img = $(this).attr('src');
        $('#subImg_subImg_in_explanation img').removeClass('focus_img');
        $('#subImg_2_subImg_in_explanation img').removeClass('focus_img');
        $(this).addClass('focus_img');

        $('#subImg_2 li').removeClass('current');
        $(this).parent().addClass('current');

        if ($('#mainImg img').length==1){
        $('#mainImg img').fadeOut(100, function() {
            $('#mainImg img').attr('src', img).on('load', function() {
                 $(this).fadeIn();
            })
       })
       }else {
        $('#mainImg').prepend('<img>');
        $('#mainImg img').attr('src', img).on('load', function() {
                 $(this).fadeIn();
            })
       }
    });
});



    window.onscroll = function() {
    var body = window.document.body;
    var html = window.document.documentElement;
    var scrollTop = body.scrollTop || html.scrollTop;
    var body_scroll_px_forms = document.getElementsByName("body_scroll_px");
    for (var i = 0; i < body_scroll_px_forms.length; i++) {
    body_scroll_px_forms[i].value = scrollTop;
    }
    }


    $(document).ready(function(){
        var scroll_position = document.getElementById("scroll_position").title;
        window.scrollTo(0,scroll_position);
        var param = location.search;
        if (param=='?status=success') {
            document.getElementById("base_message_div").innerHTML = "<p><i class='fas fa-exclamation-circle'></i>編集が完了しました。</p>";
        }
        });


function popupImageQuestion() {
  var popup = document.getElementById('js-popup');
  if(!popup) return;

  var closeBtn = document.getElementById('js-close-btn');
  var question_form = document.getElementById('id_question');

  closePopUp(closeBtn);
  openPopUp(question_form);

  var count = 0;

  function openPopUp(elem) {
    if(!elem) return;
    elem.addEventListener('focus', function() {
      if(count==1) return;
      popup.classList.add('is-show');
      count = 1;
    });
  }

  function closePopUp(elem) {
    if(!elem) return;
    elem.addEventListener('click', function() {
      popup.classList.remove('is-show');
    });
  }
}


popupImageQuestion();


function popupImageAnswer() {
  var popup = document.getElementById('js-popup');
  if(!popup) return;

  var closeBtn = document.getElementById('js-close-btn');
  var question_form = document.getElementById('id_answer');

  closePopUp(closeBtn);
  openPopUp(question_form);

  var count = 0;

  function openPopUp(elem) {
    if(!elem) return;
    elem.addEventListener('focus', function() {
      if(count==1) return;
      popup.classList.add('is-show');
      count = 1;
    });
  }

  function closePopUp(elem) {
    if(!elem) return;
    elem.addEventListener('click', function() {
      popup.classList.remove('is-show');
    });
  }
}


popupImageAnswer();



function popupBuyConfirm() {
  var popup = document.getElementById('js-popup_2');
  if(!popup) return;

  var closeBtn = document.getElementById('js-close-btn_2');
  var buy_button = document.getElementById('buy_button');

  closePopUp(closeBtn);
  openPopUp(buy_button);


  function openPopUp(elem) {
    if(!elem) return;
    elem.addEventListener('click', function() {
      popup.classList.add('is-show');
    });
  }

  function closePopUp(elem) {
    if(!elem) return;
    elem.addEventListener('click', function() {
      popup.classList.remove('is-show');
    });
  }
}


popupBuyConfirm();



