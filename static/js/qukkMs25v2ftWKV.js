var blob = null;
var blob_obj = {};


$(function() {
  $('.js-upload-file').on('change', function () {
    var file = $(this).prop('files')[0];
  });
});


function clearFile(event) {
    document.getElementById("canvas_div").classList.add("canvas_none");
    document.getElementById("user-image").classList.add("none");
    document.getElementById("preview").classList.add("none");
    document.getElementById("user-image_normal").classList.remove("none");
    document.getElementById("image_clear").value = "clear" ;
    event.preventDefault();
    $("#id_image").remove();
    blob = null;
    $("#image_span")
    .after(" <input type='file' name='image' accept='image/*' id='id_image' class='js-upload-file' onchange='previewImage(this);'>");
}

function previewImage(obj)
{
    if ($(obj).prop('files')[0]){
        file = $(obj).prop('files')[0];
        if (file.type != 'image/jpeg' && file.type != 'image/png' && file.type != 'image/svg+xml' && file.type != 'image/gif' && file.type != 'image/bmp' && file.type != 'image/tif') {
          file = null;
          blob = null;
          document.getElementById("account_none_error").innerText = 'そのファイルはアップロードできません。';
          return;
        }
    }else {
        return;
    }

    var fileReader = new FileReader();
    fileReader.onload = (function(e) {

    document.getElementById("user-image_normal").classList.add("none");
    document.getElementById("user-image").classList.add("none");
    document.getElementById("preview").classList.remove("none");
    document.getElementById("image_clear").value = "change";
    document.getElementById("canvas_div").classList.remove("canvas_none");
    document.getElementById("canvas_div").classList.add("canvas_block");

    var canvas = document.getElementById('preview');
    var ctx = canvas.getContext('2d');
    var image = new Image();
    image.src = fileReader.result;
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
            second_blob_obj = {};
            second_blob_obj.blob = blob;
            second_blob_obj.image_name = 'image';
            blob_obj.blob = second_blob_obj;
        });
        image.src = e.target.result;
    });
    fileReader.readAsDataURL(obj.files[0]);
}

  $('#account_submit_button').click(function(){

    document.getElementById("account_none_error_message").innerHTML = "<i class='fas fa-paper-plane'></i> 送信中...";

    var button = document.getElementById("account_submit_button");
    button.disabled = true

    var sell_form = document.getElementById('account_edit_form');
    var name, fd = new FormData(sell_form);

    try {
    if(blob) {
        fd.set('image', blob);
    }
    } catch {
        document.getElementById("account_none_error_message").innerText = '画像1はアップロードできません。';
    }

    $.ajax({
      url: "http://127.0.0.1:8000/account_edit/",
      type: 'POST',
      data: fd,
      processData: false,
      contentType: false,
    })
    .done((response => {
        if (response.message) {
             document.getElementById("account_none_error_message").innerText = response.message;
             button.disabled = false
             return;
            }

            location.href = "http://127.0.0.1:8000/account/?status=success"

        }))
    .fail(function( jqXHR, textStatus, errorThrown ) {
      button.disabled = false
      document.getElementById("account_none_error_message").innerText = '送信に失敗しました。';
    });

 });



