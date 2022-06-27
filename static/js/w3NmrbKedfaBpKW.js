var blob = null;
var blob_2 = null;
var blob_3 = null;
var blob_4 = null;
var blob_5 = null;
var blob_6 = null;
var blob_7 = null;
var blob_8 = null;
var blob_9 = null;
var blob_10 = null;
var blob_obj = {};


function clearFile(event) {
    document.getElementById("canvas_div").classList.add("canvas_none");
    event.preventDefault();
    document.getElementById("image_clear").value = "clear" ;
    $("#user-image").remove();
    $("#id_image").remove();
    blob = null;
    $("#image_span")
    .after(" <input type='file' name='image' accept='image/*' id='id_image' class='js-upload-file' onchange='previewImage(this);'>");
    document.getElementById("required_message").classList.remove("none");
}

function previewImage(obj)
{
    if ($(obj).prop('files')[0]){
        file = $(obj).prop('files')[0];
        if (file.type != 'image/jpeg' && file.type != 'image/png' && file.type != 'image/svg+xml' && file.type != 'image/gif' && file.type != 'image/bmp' && file.type != 'image/tif') {
          file = null;
          blob = null;
          document.getElementById("talk_none_error").innerText = 'そのファイルはアップロードできません。';

          return;
        }
    }else {

        return;
    }

    var fileReader = new FileReader();
    fileReader.onload = (function(e) {
        $("#user-image").remove();
        document.getElementById("image_clear").value = "" ;
        document.getElementById("canvas_div").classList.remove("canvas_none");
        document.getElementById("canvas_div").classList.add("canvas_block");
        document.getElementById("camera_icon_2").classList.add("display");
        document.getElementById("image_cancel_icon_2").classList.add("display");
        document.getElementById("required_message").classList.add("none");

        if (document.defaultView.getComputedStyle(document.getElementById("canvas_div_2"),null).display == 'none') {
            $("#image_span_2")
            .after(" <input type='file' name='image_2' accept='image/*' id='id_image_2' class='js-upload-file' onchange='previewImage_2(this);'>");
        }

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




function clearFile_2(event) {
    document.getElementById("canvas_div_2").classList.add("canvas_none");
    event.preventDefault();
    document.getElementById("image_clear_2").value = "clear" ;
    $("#user-image_2").remove();
    $("#id_image_2").remove();
    blob_2 = null;
    $("#image_span_2")
    .after(" <input type='file' name='image_2' accept='image/*' id='id_image_2' class='js-upload-file' onchange='previewImage_2(this);'>");
}

function previewImage_2(obj)
{
        if ($(obj).prop('files')[0]){
            file = $(obj).prop('files')[0];
            if (file.type != 'image/jpeg' && file.type != 'image/png' && file.type != 'image/svg+xml' && file.type != 'image/gif' && file.type != 'image/bmp' && file.type != 'image/tif') {
              file = null;
              blob_2 = null;
              document.getElementById("talk_none_error").innerText = 'そのファイルはアップロードできません。';
              return;
            }
        }else {
            return;
        }

    var fileReader = new FileReader();
    fileReader.onload = (function(e) {
        $("#user-image_2").remove();
        document.getElementById("image_clear_2").value = "" ;
        document.getElementById("canvas_div_2").classList.remove("canvas_none");
        document.getElementById("canvas_div_2").classList.add("canvas_block");
        document.getElementById("camera_icon_3").classList.add("display");
        document.getElementById("image_cancel_icon_3").classList.add("display");
        if (document.defaultView.getComputedStyle(document.getElementById("canvas_div_3"),null).display == 'none') {
        $("#image_span_3")
        .after(" <input type='file' name='image_3' accept='image/*' id='id_image_3' class='js-upload-file' onchange='previewImage_3(this);'>");
        }
        var canvas = document.getElementById('preview_2');
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
                blob_2 = new Blob([barr], {type: 'image/jpeg'});
                second_blob_obj = {};
                second_blob_obj.blob = blob_2;
                second_blob_obj.image_name = 'image_2';
                blob_obj.blob_2 = second_blob_obj;
            });
            image.src = e.target.result;
    });
    fileReader.readAsDataURL(obj.files[0]);
}




function clearFile_3(event) {
    document.getElementById("canvas_div_3").classList.add("canvas_none");
    event.preventDefault();
    document.getElementById("image_clear_3").value = "clear" ;
    $("#user-image_3").remove();
    $("#id_image_3").remove();
    blob_3 = null;
    $("#image_span_3")
    .after(" <input type='file' name='image_3' accept='image/*' id='id_image_3' class='js-upload-file' onchange='previewImage_3(this);'>");
}

function previewImage_3(obj)
{
        if ($(obj).prop('files')[0]){
            file = $(obj).prop('files')[0];
            if (file.type != 'image/jpeg' && file.type != 'image/png' && file.type != 'image/svg+xml' && file.type != 'image/gif' && file.type != 'image/bmp' && file.type != 'image/tif') {
              file = null;
              blob_3 = null;
              document.getElementById("talk_none_error").innerText = 'そのファイルはアップロードできません。';
              return;
            }
        }else {
            return;
        }

    var fileReader = new FileReader();
    fileReader.onload = (function(e) {
        $("#user-image_3").remove();
        document.getElementById("image_clear_3").value = "" ;
        document.getElementById("canvas_div_3").classList.remove("canvas_none");
        document.getElementById("canvas_div_3").classList.add("canvas_block");
        document.getElementById("camera_icon_4").classList.add("display");
        document.getElementById("image_cancel_icon_4").classList.add("display");
        if (document.defaultView.getComputedStyle(document.getElementById("canvas_div_4"),null).display == 'none') {
        $("#image_span_4")
        .after(" <input type='file' name='image_4' accept='image/*' id='id_image_4' class='js-upload-file' onchange='previewImage_4(this);'>");
        }
        var canvas = document.getElementById('preview_3');
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
                blob_3 = new Blob([barr], {type: 'image/jpeg'});
                second_blob_obj = {};
                second_blob_obj.blob = blob_3;
                second_blob_obj.image_name = 'image_3';
                blob_obj.blob_3 = second_blob_obj;

            });
            image.src = e.target.result;
    });
    fileReader.readAsDataURL(obj.files[0]);
}


function clearFile_4(event) {
    document.getElementById("canvas_div_4").classList.add("canvas_none");
    event.preventDefault();
    document.getElementById("image_clear_4").value = "clear" ;
    $("#user-image_4").remove();
    $("#id_image_4").remove();
    blob_4 = null;
    $("#image_span_4")
    .after(" <input type='file' name='image_4' accept='image/*' id='id_image_4' class='js-upload-file' onchange='previewImage_4(this);'>");
}

function previewImage_4(obj)
{
        if ($(obj).prop('files')[0]){
            file = $(obj).prop('files')[0];
            if (file.type != 'image/jpeg' && file.type != 'image/png' && file.type != 'image/svg+xml' && file.type != 'image/gif' && file.type != 'image/bmp' && file.type != 'image/tif') {
              file = null;
              blob_4 = null;
              document.getElementById("talk_none_error").innerText = 'そのファイルはアップロードできません。';
              return;
            }
        }else {
                    　
            return;
        }

    var fileReader = new FileReader();
    fileReader.onload = (function(e) {
        $("#user-image_4").remove();
        document.getElementById("image_clear_4").value = "" ;
        document.getElementById("canvas_div_4").classList.remove("canvas_none");
        document.getElementById("canvas_div_4").classList.add("canvas_block");
        document.getElementById("camera_icon_5").classList.add("display");
        document.getElementById("image_cancel_icon_5").classList.add("display");
        if (document.defaultView.getComputedStyle(document.getElementById("canvas_div_5"),null).display == 'none') {
        $("#image_span_5")
        .after(" <input type='file' name='image_5' accept='image/*' id='id_image_5' class='js-upload-file' onchange='previewImage_5(this);'>");
        }
        var canvas = document.getElementById('preview_4');
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
                blob_4 = new Blob([barr], {type: 'image/jpeg'});
                second_blob_obj = {};
                second_blob_obj.blob = blob_4;
                second_blob_obj.image_name = 'image_4';
                blob_obj.blob_4 = second_blob_obj;
            });
            image.src = e.target.result;
    });
    fileReader.readAsDataURL(obj.files[0]);
}



function clearFile_5(event) {
    document.getElementById("canvas_div_5").classList.add("canvas_none");
    event.preventDefault();
    document.getElementById("image_clear_5").value = "clear" ;
    $("#user-image_5").remove();
    $("#id_image_5").remove();
    blob_5 = null;
    $("#image_span_5")
    .after(" <input type='file' name='image_5' accept='image/*' id='id_image_5' class='js-upload-file' onchange='previewImage_5(this);'>");
}

function previewImage_5(obj)
{
        if ($(obj).prop('files')[0]){
            file = $(obj).prop('files')[0];
            if (file.type != 'image/jpeg' && file.type != 'image/png' && file.type != 'image/svg+xml' && file.type != 'image/gif' && file.type != 'image/bmp' && file.type != 'image/tif') {
              file = null;
              blob_5 = null;
              document.getElementById("talk_none_error").innerText = 'そのファイルはアップロードできません。';
              return;
            }
        }else {
                    　
            return;
        }

    var fileReader = new FileReader();
    fileReader.onload = (function(e) {
        $("#user-image_5").remove();
        document.getElementById("image_clear_5").value = "" ;
        document.getElementById("canvas_div_5").classList.remove("canvas_none");
        document.getElementById("canvas_div_5").classList.add("canvas_block");
        document.getElementById("camera_icon_6").classList.add("display");
        document.getElementById("image_cancel_icon_6").classList.add("display");
        if (document.defaultView.getComputedStyle(document.getElementById("canvas_div_6"),null).display == 'none') {
        $("#image_span_6")
        .after(" <input type='file' name='image_6' accept='image/*' id='id_image_6' class='js-upload-file' onchange='previewImage_6(this);'>");
        }
        var canvas = document.getElementById('preview_5');
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
                blob_5 = new Blob([barr], {type: 'image/jpeg'});
                second_blob_obj = {};
                second_blob_obj.blob = blob_5;
                second_blob_obj.image_name = 'image_5';
                blob_obj.blob_5 = second_blob_obj;
            });
            image.src = e.target.result;
    });
    fileReader.readAsDataURL(obj.files[0]);
}





function clearFile_6(event) {
    document.getElementById("canvas_div_6").classList.add("canvas_none");
    event.preventDefault();
    document.getElementById("image_clear_6").value = "clear" ;
    $("#user-image_6").remove();
    $("#id_image_6").remove();
    blob_6 = null;
    $("#image_span_6")
    .after(" <input type='file' name='image_6' accept='image/*' id='id_image_6' class='js-upload-file' onchange='previewImage_6(this);'>");
}

function previewImage_6(obj)
{
        if ($(obj).prop('files')[0]){
            file = $(obj).prop('files')[0];
            if (file.type != 'image/jpeg' && file.type != 'image/png' && file.type != 'image/svg+xml' && file.type != 'image/gif' && file.type != 'image/bmp' && file.type != 'image/tif') {
              file = null;
              blob_6 = null;
              document.getElementById("talk_none_error").innerText = 'そのファイルはアップロードできません。';
              return;
            }
        }else {
            return;
        }

    var fileReader = new FileReader();
    fileReader.onload = (function(e) {
        $("#user-image_6").remove();
        document.getElementById("image_clear_6").value = "" ;
        document.getElementById("canvas_div_6").classList.remove("canvas_none");
        document.getElementById("canvas_div_6").classList.add("canvas_block");
        document.getElementById("camera_icon_7").classList.add("display");
        document.getElementById("image_cancel_icon_7").classList.add("display");
        if (document.defaultView.getComputedStyle(document.getElementById("canvas_div_7"),null).display == 'none') {
        $("#image_span_7")
        .after(" <input type='file' name='image_7' accept='image/*' id='id_image_7' class='js-upload-file' onchange='previewImage_7(this);'>");
        }
        var canvas = document.getElementById('preview_6');
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
                blob_6 = new Blob([barr], {type: 'image/jpeg'});
                second_blob_obj = {};
                second_blob_obj.blob = blob_6;
                second_blob_obj.image_name = 'image_6';
                blob_obj.blob_6 = second_blob_obj;
            });
            image.src = e.target.result;
    });
    fileReader.readAsDataURL(obj.files[0]);
}



function clearFile_7(event) {
    document.getElementById("canvas_div_7").classList.add("canvas_none");
    event.preventDefault();
    document.getElementById("image_clear_7").value = "clear" ;
    $("#user-image_7").remove();
    $("#id_image_7").remove();
    blob_7 = null;
    $("#image_span_7")
    .after(" <input type='file' name='image_7' accept='image/*' id='id_image_7' class='js-upload-file' onchange='previewImage_7(this);'>");
}

function previewImage_7(obj)
{
        if ($(obj).prop('files')[0]){
            file = $(obj).prop('files')[0];
            if (file.type != 'image/jpeg' && file.type != 'image/png' && file.type != 'image/svg+xml' && file.type != 'image/gif' && file.type != 'image/bmp' && file.type != 'image/tif') {
              file = null;
              blob_7 = null;
              document.getElementById("talk_none_error").innerText = 'そのファイルはアップロードできません。';
              return;
            }
        }else {
            return;
        }

    var fileReader = new FileReader();
    fileReader.onload = (function(e) {
        $("#user-image_7").remove();
        document.getElementById("image_clear_7").value = "" ;
        document.getElementById("canvas_div_7").classList.remove("canvas_none");
        document.getElementById("canvas_div_7").classList.add("canvas_block");
        document.getElementById("camera_icon_8").classList.add("display");
        document.getElementById("image_cancel_icon_8").classList.add("display");
        if (document.defaultView.getComputedStyle(document.getElementById("canvas_div_8"),null).display == 'none') {
        $("#image_span_8")
        .after(" <input type='file' name='image_8' accept='image/*' id='id_image_8' class='js-upload-file' onchange='previewImage_8(this);'>");
        }
        var canvas = document.getElementById('preview_7');
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
                blob_7 = new Blob([barr], {type: 'image/jpeg'});
                second_blob_obj = {};
                second_blob_obj.blob = blob_7;
                second_blob_obj.image_name = 'image_7';
                blob_obj.blob_7 = second_blob_obj;
            });
            image.src = e.target.result;
    });
    fileReader.readAsDataURL(obj.files[0]);
}



function clearFile_8(event) {
    document.getElementById("canvas_div_8").classList.add("canvas_none");
    event.preventDefault();
    document.getElementById("image_clear_8").value = "clear" ;
    $("#user-image_8").remove();
    $("#id_image_8").remove();
    blob_8 = null;
    $("#image_span_8")
    .after(" <input type='file' name='image_8' accept='image/*' id='id_image_8' class='js-upload-file' onchange='previewImage_8(this);'>");
}

function previewImage_8(obj)
{
        if ($(obj).prop('files')[0]){
            file = $(obj).prop('files')[0];
            if (file.type != 'image/jpeg' && file.type != 'image/png' && file.type != 'image/svg+xml' && file.type != 'image/gif' && file.type != 'image/bmp' && file.type != 'image/tif') {
              file = null;
              blob_8 = null;
              document.getElementById("talk_none_error").innerText = 'そのファイルはアップロードできません。';
              return;
            }
        }else {
            return;
        }

    var fileReader = new FileReader();
    fileReader.onload = (function(e) {
        $("#user-image_8").remove();
        document.getElementById("image_clear_8").value = "" ;
        document.getElementById("canvas_div_8").classList.remove("canvas_none");
        document.getElementById("canvas_div_8").classList.add("canvas_block");
        document.getElementById("camera_icon_9").classList.add("display");
        document.getElementById("image_cancel_icon_9").classList.add("display");
        if (document.defaultView.getComputedStyle(document.getElementById("canvas_div_9"),null).display == 'none') {
        $("#image_span_9")
        .after(" <input type='file' name='image_9' accept='image/*' id='id_image_9' class='js-upload-file' onchange='previewImage_9(this);'>");
        }
        var canvas = document.getElementById('preview_8');
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
                blob_8 = new Blob([barr], {type: 'image/jpeg'});
                second_blob_obj = {};
                second_blob_obj.blob = blob_8;
                second_blob_obj.image_name = 'image_8';
                blob_obj.blob_8 = second_blob_obj;
            });
            image.src = e.target.result;
    });
    fileReader.readAsDataURL(obj.files[0]);
}



function clearFile_9(event) {
    document.getElementById("canvas_div_9").classList.add("canvas_none");
    event.preventDefault();
    document.getElementById("image_clear_9").value = "clear" ;
    $("#user-image_9").remove();
    $("#id_image_9").remove();
    blob_9 = null;
    $("#image_span_9")
    .after(" <input type='file' name='image_9' accept='image/*' id='id_image_9' class='js-upload-file' onchange='previewImage_9(this);'>");
}

function previewImage_9(obj)
{
        if ($(obj).prop('files')[0]){
            file = $(obj).prop('files')[0];
            if (file.type != 'image/jpeg' && file.type != 'image/png' && file.type != 'image/svg+xml' && file.type != 'image/gif' && file.type != 'image/bmp' && file.type != 'image/tif') {
              file = null;
              blob_9 = null;
              document.getElementById("talk_none_error").innerText = 'そのファイルはアップロードできません。';
              return;
            }
        }else {
            return;
        }

    var fileReader = new FileReader();
    fileReader.onload = (function(e) {
        $("#user-image_9").remove();
        document.getElementById("image_clear_9").value = "" ;
        document.getElementById("canvas_div_9").classList.remove("canvas_none");
        document.getElementById("canvas_div_9").classList.add("canvas_block");
        document.getElementById("camera_icon_10").classList.add("display");
        document.getElementById("image_cancel_icon_10").classList.add("display");
        if (document.defaultView.getComputedStyle(document.getElementById("canvas_div_10"),null).display == 'none') {
        $("#image_span_10")
        .after(" <input type='file' name='image_10' accept='image/*' id='id_image_10' class='js-upload-file' onchange='previewImage_10(this);'>");
        }
        var canvas = document.getElementById('preview_9');
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
                blob_9 = new Blob([barr], {type: 'image/jpeg'});
                second_blob_obj = {};
                second_blob_obj.blob = blob_9;
                second_blob_obj.image_name = 'image_9';
                blob_obj.blob_9 = second_blob_obj;
            });
            image.src = e.target.result;
    });
    fileReader.readAsDataURL(obj.files[0]);
}



function clearFile_10(event) {
    document.getElementById("canvas_div_10").classList.add("canvas_none");
    event.preventDefault();
    document.getElementById("image_clear_10").value = "clear" ;
    $("#user-image_10").remove();
    $("#id_image_10").remove();
    blob_10 = null;
    $("#image_span_10")
    .after(" <input type='file' name='image_10' accept='image/*' id='id_image_10' class='js-upload-file' onchange='previewImage_10(this);'>");
}

function previewImage_10(obj)
{
        if ($(obj).prop('files')[0]){
            file = $(obj).prop('files')[0];
            if (file.type != 'image/jpeg' && file.type != 'image/png' && file.type != 'image/svg+xml' && file.type != 'image/gif' && file.type != 'image/bmp' && file.type != 'image/tif') {
              file = null;
              blob_10 = null;
              document.getElementById("talk_none_error").innerText = 'そのファイルはアップロードできません。';
              return;
            }
        }else {
            return;
        }

    var fileReader = new FileReader();
    fileReader.onload = (function(e) {
        $("#user-image_10").remove();
        document.getElementById("image_clear_10").value = "" ;
        document.getElementById("canvas_div_10").classList.remove("canvas_none");
        document.getElementById("canvas_div_10").classList.add("canvas_block");
        var canvas = document.getElementById('preview_10');
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
                blob_10 = new Blob([barr], {type: 'image/jpeg'});
                second_blob_obj = {};
                second_blob_obj.blob = blob_10;
                second_blob_obj.image_name = 'image_10';
                blob_obj.blob_10 = second_blob_obj;
            });
            image.src = e.target.result;
    });
    fileReader.readAsDataURL(obj.files[0]);
}





  $('#sell_form_submit_button').click(function(){
    var merchandise_name = document.getElementById("id_merchandise_name").value;
    var value = document.getElementById("id_value").value;
    var merchandise_status = document.getElementById("id_merchandise_status").value;
    var category = document.getElementById("id_category").value;
    var region = document.getElementById("id_region").value;
    var explanation = document.getElementById("id_explanation").value;

    if (!blob){
        document.getElementById("sell_form_error").innerHTML = "<i class='fas fa-exclamation-circle'></i>商品のトップ画像は必須です。";
        return false;
    }
    if (!merchandise_name){
        document.getElementById("sell_form_error").innerHTML = "<i class='fas fa-exclamation-circle'></i>商品名は必須です。";
        return false;
    }
    if (!value){
        document.getElementById("sell_form_error").innerHTML = "<i class='fas fa-exclamation-circle'></i>価格は必須です。";
        return false;
    }
    if (!merchandise_status){
        document.getElementById("sell_form_error").innerHTML = "<i class='fas fa-exclamation-circle'></i>商品の状態は必須です。";
        return false;
    }
    if (!category){
        document.getElementById("sell_form_error").innerHTML = "<i class='fas fa-exclamation-circle'></i>カテゴリは必須です。";
        return false;
    }
    if (!region){
        document.getElementById("sell_form_error").innerHTML = "<i class='fas fa-exclamation-circle'></i>商品の受け渡しが可能なエリアは必須です。";
        return false;
    }
    if (!explanation){
        document.getElementById("sell_form_error").innerHTML = "<i class='fas fa-exclamation-circle'></i>商品説明は必須です。";
        return false;
    }

    document.getElementById("sell_form_error").innerHTML = "<i class='fas fa-paper-plane'></i> 送信中...";

    var button = document.getElementById("sell_form_submit_button");
    button.disabled = true

    var sell_form = document.getElementById('sell_form');
    var name, fd = new FormData(sell_form);
    try {
    if(blob) {
        fd.set('image', blob);
    }
    } catch {
        document.getElementById("sell_form_error").innerText = '画像1はアップロードできません。';
    }
    try {
    if(blob_2) {
        fd.set('image_2', blob_2);
    }
    } catch {
        document.getElementById("sell_form_error").innerText = '画像2はアップロードできません。';
    }
    try {
    if(blob_3) {
        fd.set('image_3', blob_3);
    }
    } catch {
        document.getElementById("sell_form_error").innerText = '画像3はアップロードできません。';
    }
    try {
    if(blob_4) {
        fd.set('image_4', blob_4);
    }
    } catch {
        document.getElementById("sell_form_error").innerText = '画像4はアップロードできません。';
    }
    try {
    if(blob_5) {
        fd.set('image_5', blob_5);
    }
    } catch {
        document.getElementById("sell_form_error").innerText = '画像5はアップロードできません。';
    }
    try {
    if(blob_6) {
        fd.set('image_6', blob_6);
    }
    } catch {
        document.getElementById("sell_form_error").innerText = '画像6はアップロードできません。';
    }
    try {
    if(blob_7) {
        fd.set('image_7', blob_7);
    }
    } catch {
        document.getElementById("sell_form_error").innerText = '画像7はアップロードできません。';
    }
    try {
    if(blob_8) {
        fd.set('image_8', blob_8);
    }
    } catch {
        document.getElementById("sell_form_error").innerText = '画像8はアップロードできません。';
    }
    try {
    if(blob_9) {
        fd.set('image_9', blob_9);
    }
    } catch {
        document.getElementById("sell_form_error").innerText = '画像9はアップロードできません。';
    }
    try {
    if(blob_10) {
        fd.set('image_10', blob_10);
    }
    } catch {
        document.getElementById("sell_form_error").innerText = '画像10はアップロードできません。';
    }

    $.ajax({
      url: "http://127.0.0.1:8000/sell_save/",
      type: 'POST',
      data: fd,
      processData: false,
      contentType: false,
    })
    .done((response => {
        if (response.message) {
             document.getElementById("sell_form_error").innerText = response.message;
             button.disabled = false
             return;
            }

            location.href = "http://127.0.0.1:8000/sell_list/?status=success"

        }))
    .fail(function( jqXHR, textStatus, errorThrown ) {
      button.disabled = false
      document.getElementById("sell_form_error").innerText = '送信に失敗しました。';
    });

 });


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function FacultyChangeSelection(){
    var select_box = document.getElementById("id_faculty");
    var index = select_box.selectedIndex;
    var text = select_box.options[index].text;
    if (text=='追加する') {
        $('#id_department > option').remove();
        $('#id_department').append($('<option>').html("選択して下さい").val(""));
        $('#id_department').append($('<option>').html("追加する").val(""));
        document.getElementById("plus_faculty_input").classList.remove("none");
        return;
    }
    document.getElementById("plus_faculty_input").classList.add("none");
    const csrftoken = getCookie('csrftoken');

    fd = new FormData();
    fd.set('faculty', document.getElementById("id_faculty").value)
    $.ajax({
          url: "http://127.0.0.1:8000/department_selections/",
          type: 'POST',
          headers: {'X-CSRFToken': csrftoken},
          data: fd,
          processData: false,
          contentType: false,
        })
        .done((response => {

              $('#id_department > option').remove();
              $('#id_department').append($('<option>').html("選択して下さい").val(""));

              var department_list = response.department_list;
              var count=1;
              for( var department in department_list ) {
                        $('#id_department').append($('<option>').html(department_list[department]).val(department_list[department]));
                        count++;
                }
　             $('#id_department').append($('<option>').html("追加する").val(""));

        }))
        .fail(function( jqXHR, textStatus, errorThrown ) {
        });
}


var faculty_selection = document.getElementById("id_faculty");
faculty_selection.onchange=FacultyChangeSelection;



function DepartmentChangeSelection(){
    var select_box = document.getElementById("id_department");
    var index = select_box.selectedIndex;
    var text = select_box.options[index].text;
    if (text=='追加する') {
        document.getElementById("plus_department_input").classList.remove("none");
        return;
    }
    document.getElementById("plus_department_input").classList.add("none");
}

var department_selection = document.getElementById("id_department");
department_selection.onchange=DepartmentChangeSelection;
