function ExistJudge1() {
    var val = $(this).val();
    $.ajax({
        url: "http://127.0.0.1:8000/check_username/",
        type: 'GET',
        data: {
            'entered_username': val,
        }
    }).done(response => {
                            if (response.Username == 1) {
                                $('#exist1').empty();
                                $('#exist1').append('<span id=not_exist><i class="fas fa-exclamation-circle"></i>すでに使用されています。</span>');
                            }else if(response.Username == 0){
                                $('#exist1').empty();
                                $('#exist1').append('<i class="far fa-check-circle"></i>');}
                        });
};
$(function() {
  $('#id_username').keyup(ExistJudge1);
});
