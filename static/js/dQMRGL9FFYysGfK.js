    window.onscroll = function() {
    var body = window.document.body;
    var html = window.document.documentElement;
    var scrollTop = body.scrollTop || html.scrollTop;
    var body_scroll_px_forms = document.getElementsByName("body_scroll_px");
    for (var i = 0; i < body_scroll_px_forms.length; i++) {
    body_scroll_px_forms[i].value = scrollTop;  //name="body_scroll_px"のinputのvalueに自動的にスクロールが何pxか表示されるよう指定
    }
    }


    window.onscroll = function() {
    var body = window.document.body;
    var html = window.document.documentElement;
    var scrollTop = body.scrollTop || html.scrollTop;
    var scroll_position = document.getElementById("scroll_position");
    scroll_position.title = scrollTop;
    }



$(document).ready(function(){
    var scroll_position = document.getElementById("scroll_position").title;
    window.scrollTo(0,scroll_position);
    });


function refund_request_check(){

	if(window.confirm('リクエスト送信後、運営が審査し、登録メールアドレスに結果を返信いたします。またリクエストを送信するとトーク機能が停止されます。\r\n返金リクエストを送信しますか？')){

		return true;

	}
	else{

		return false;

	}

}





$(function(){
    $('#subImg img').on('click',function(){

        img = $(this).attr('src');

        $('#subImg li').removeClass('current');
        $(this).parent().addClass('current');

        $('#mainImg img').fadeOut(50, function() {
            $('#mainImg img').attr('src', img).on('load', function() {
                 $(this).fadeIn();
            })
       })
    });
});


$(function(){
    $('#subImg_2 img').on('click',function(){

        img = $(this).attr('src');

        $('#subImg_2 li').removeClass('current');
        $(this).parent().addClass('current');

        $('#mainImg img').fadeOut(50, function() {
            $('#mainImg img').attr('src', img).on('load', function() {
                 $(this).fadeIn();
            })
       })
    });
});


function hidden_or_visible(){

    document.getElementById("more_wrap").classList.toggle("more_visible");

}




var blob = null;

    function talk_image_clearFile(event) {
        document.getElementById("canvas_div_2").classList.add("canvas_none");
        event.preventDefault();
        $("#talk_image").remove();
        $("#talk_image_span")
        .after(" <input type='file' name='talk_image' accept='image/*' id='talk_image' class='talk_js-upload-file none' onchange='talk_preview_Image(this)'>");
    }

    function talk_preview_Image(obj)
    {
        if ($(obj).prop('files')[0]){
            file = $(obj).prop('files')[0];
            if (file.type != 'image/jpeg' && file.type != 'image/png' && file.type != 'image/svg+xml' && file.type != 'image/gif' && file.type != 'image/bmp' && file.type != 'image/tif') {
              file = null;
              blob = null;
              document.getElementById("talk_none_error").innerText = 'そのファイルはアップロードできません。';
          　　
            　document.getElementById("canvas_div_2").classList.add("canvas_none");
            　event.preventDefault();
            　$("#talk_image").remove();
            　$("#talk_image_span")
            　.after(" <input type='file' name='talk_image' accept='image/*' id='talk_image' class='talk_js-upload-file none' onchange='talk_preview_Image(this)'>");

              return;
            }
        }else {
                    　
            　document.getElementById("canvas_div_2").classList.add("canvas_none");
            　event.preventDefault();
            　$("#talk_image").remove();
            　$("#talk_image_span")
            　.after(" <input type='file' name='talk_image' accept='image/*' id='talk_image' class='talk_js-upload-file none' onchange='talk_preview_Image(this)'>");

            return;
        }

        document.getElementById("talk_none_error").innerText = '';

        var fileReader = new FileReader();
        fileReader.onload = (function(e) {
            document.getElementById("canvas_div_2").classList.remove("canvas_none");
            document.getElementById("canvas_div_2").classList.add("canvas_block");

            var canvas = document.getElementById('preview_2');
            var ctx = canvas.getContext('2d');
            var image = new Image();

            image.onload = (function () {

                const THUMBNAIL_MAX_WIDTH = 300;
                const THUMBNAIL_MAX_HEIGHT = 300;

                var width, height;
                if(image.width > image.height){
                  var ratio = image.height/image.width;
                  width = THUMBNAIL_MAX_WIDTH;
                  height = THUMBNAIL_MAX_WIDTH * ratio;
                } else {
                  var ratio = image.width/image.height;
                  width = THUMBNAIL_MAX_HEIGHT * ratio;
                  height = THUMBNAIL_MAX_HEIGHT;
                }

                canvas.width = width;
                canvas.height = height;

                ctx.drawImage(image, 0, 0, image.width, image.height, 0, 0, width, height);

                var base64 = canvas.toDataURL('image/png');
                var barr, bin, i, len;
                bin = atob(base64.split('base64,')[1]);
                len = bin.length;
                barr = new Uint8Array(len);
                i = 0;
                while (i < len) {
                  barr[i] = bin.charCodeAt(i);
                  i++;
                }
                blob = new Blob([barr], {type: 'image/jpeg'});
            });
            image.src = e.target.result;

        });
        fileReader.readAsDataURL(obj.files[0]);
    }


      $('#talk_submit_button').click(function(){

        var image = document.getElementById("talk_image").value;
        var comment = document.getElementById("id_comment").value;

        if(comment == false){
            if (!image){
                document.getElementById("talk_none_error").innerText = 'コメント・画像がありません。';
                return;
            }
        }

        document.getElementById("talk_none_error").innerHTML = "<i class='fas fa-paper-plane'></i> 送信中...";

        var button = document.getElementById("talk_submit_button");
        button.disabled = true

        var comment_form = document.getElementById('comment_form');
        var name, fd = new FormData(comment_form);
        try {
        if(blob) {
            fd.set('talk_image', blob);
        }
        } catch {
            document.getElementById("talk_none_error").innerText = 'その画像はアップロードできません。';
        }

        var scroll_position = document.getElementById("scroll_position").title;
        $.ajax({
          url: "http://127.0.0.1:8000/talk_room_post/",
          type: 'POST',
          data: fd,
          processData: false,
          contentType: false,
        })
        .done((response => {
            if (response.message) {
                 document.getElementById("talk_none_error").innerText = response.message;
                 button.disabled = false
                 return;
                }
              location.reload();
              window.scrollTo(0,scroll_position);
        }))
        .fail(function( jqXHR, textStatus, errorThrown ) {
          button.disabled = false
          document.getElementById("talk_none_error").innerText = '送信に失敗しました。';
        });

     });


function popupImage() {
  var popup = document.getElementById('js-popup');
  if(!popup) return;

  var closeBtn = document.getElementById('js-close-btn');
  var refund_form_button = document.getElementById('refund_form_button');

  closePopUp(closeBtn);
  openPopUp(refund_form_button);


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


popupImage();



function clearFile(event) {
    document.getElementById("canvas_div").classList.add("canvas_none");
    event.preventDefault();
    $("#user-image").remove();
    $("#id_image").remove();
    $("#image_span")
    .after(" <input type='file' name='image_for_refund' accept='image/*' id='id_image' class='js-upload-file' onchange='previewImage(this);'>");
}



function previewImage(obj)
{
    var fileReader = new FileReader();
    fileReader.onload = (function() {
        $("#user-image").remove();
        document.getElementById("canvas_div").classList.remove("canvas_none");
        document.getElementById("canvas_div").classList.add("canvas_block");

        var canvas = document.getElementById('preview');
        var ctx = canvas.getContext('2d');
        var image = new Image();
        image.src = fileReader.result;
        image.onload = (function () {
            canvas.width = image.width;
            canvas.height = image.height;
            ctx.drawImage(image, 0, 0);
        });
    });
    fileReader.readAsDataURL(obj.files[0]);
}


var blob2 = null;

    function previewImage(obj)
    {
        if ($(obj).prop('files')[0]){
            file = $(obj).prop('files')[0];
            if (file.type != 'image/jpeg' && file.type != 'image/png' && file.type != 'image/svg+xml' && file.type != 'image/gif' && file.type != 'image/bmp' && file.type != 'image/tif') {
              file = null;
              blob2 = null;
              document.getElementById("refund_error").innerText = 'そのファイルはアップロードできません。';
          　　
            document.getElementById("canvas_div").classList.add("canvas_none");
            event.preventDefault();
            $("#user-image").remove();
            $("#id_image").remove();
            $("#image_span")
            .after(" <input type='file' name='image_for_refund' accept='image/*' id='id_image' class='js-upload-file' onchange='previewImage(this);'>");
              return;
            }
        }else {
                    　
            document.getElementById("canvas_div").classList.add("canvas_none");
            event.preventDefault();
            $("#user-image").remove();
            $("#id_image").remove();
            $("#image_span")
            .after(" <input type='file' name='image_for_refund' accept='image/*' id='id_image' class='js-upload-file' onchange='previewImage(this);'>");

            return;
        }

        document.getElementById("refund_error").innerText = '';

        var fileReader = new FileReader();
        fileReader.onload = (function(e) {
            document.getElementById("canvas_div").classList.remove("canvas_none");
            document.getElementById("canvas_div").classList.add("canvas_block");

            var canvas = document.getElementById('preview');
            var ctx = canvas.getContext('2d');
            var image = new Image();

            image.onload = (function () {

                const THUMBNAIL_MAX_WIDTH = 300;
                const THUMBNAIL_MAX_HEIGHT = 300;

                var width, height;
                if(image.width > image.height){
                  var ratio = image.height/image.width;
                  width = THUMBNAIL_MAX_WIDTH;
                  height = THUMBNAIL_MAX_WIDTH * ratio;
                } else {
                  var ratio = image.width/image.height;
                  width = THUMBNAIL_MAX_HEIGHT * ratio;
                  height = THUMBNAIL_MAX_HEIGHT;
                }

                canvas.width = width;
                canvas.height = height;

                ctx.drawImage(image, 0, 0, image.width, image.height, 0, 0, width, height);

                var base64 = canvas.toDataURL('image/png');
                var barr, bin, i, len;
                bin = atob(base64.split('base64,')[1]);
                len = bin.length;
                barr = new Uint8Array(len);
                i = 0;
                while (i < len) {
                  barr[i] = bin.charCodeAt(i);
                  i++;
                }
                blob2 = new Blob([barr], {type: 'image/jpeg'});
            });
            image.src = e.target.result;

        });
        fileReader.readAsDataURL(obj.files[0]);
    }

      $('#refund_request_button').click(function(){

        var image = document.getElementById("id_image").value;
        var cases = document.getElementById("cases").value;

        if(cases == 'はい'){
            if (!image){
                document.getElementById("refund_error").innerText = '画像のアップロードは必須です。';
                return;
            }
        } else if(!cases) {
                document.getElementById("refund_error").innerText = '選択してください。';
                return;
          } else {
                document.getElementById("refund_error").innerHTML = "<i class='fas fa-paper-plane'></i> 送信中...";
                var button = document.getElementById("refund_request_button");
                button.disabled = true
          }

        document.getElementById("refund_error").innerHTML = "<i class='fas fa-paper-plane'></i> 送信中...";

        var button = document.getElementById("refund_request_button");
        button.disabled = true

        var comment_form = document.getElementById('refund_form');
        var name, fd = new FormData(comment_form);
        try {
        if(blob2) {
            fd.set('talk_image', blob2);
        }
        } catch {
            document.getElementById("refund_error").innerText = 'その画像はアップロードできません。';
        }

        var scroll_position = document.getElementById("scroll_position").title;
        $.ajax({
          url: "http://127.0.0.1:8000/refund_request/",
          type: 'POST',
          data: fd,
          processData: false,
          contentType: false,
        })
        .done((response => {
            if (response.message) {
                 document.getElementById("refund_error").innerText = response.message;
                 button.disabled = false
                 return;
                }
              location.reload();
              window.scrollTo(0,scroll_position);
        }))
        .fail(function( jqXHR, textStatus, errorThrown ) {
          button.disabled = false
          document.getElementById("refund_error").innerText = '送信に失敗しました。';
        });

     });







function selectChange(){
    var cases = document.getElementById("cases").value;
    if(cases == 'はい'){
        document.getElementById("submit_image_wrap").classList.remove("none");
    }
    else{
        document.getElementById("submit_image_wrap").classList.add("none");
    }
}


function merchandise_info_open(){

    document.getElementById("merchandise_info_wrap").classList.toggle("none");

}
