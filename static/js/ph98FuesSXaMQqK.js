function retire_check(){

	if(window.confirm('本当に退会しますか？')){

		return true;

	}
	else{

		return false;

	}

}


$(document).ready(function(){
        var param = location.search;
        if (param=='?status=success') {
            document.getElementById("base_message_div").innerHTML = "<p><i class='fas fa-exclamation-circle'></i>アカウント情報を更新しました。</p>";
        }
    });
