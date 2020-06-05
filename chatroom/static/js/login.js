$uname=$("#username");
$pwd=$("#password");
$("#btn_login").click(
function (){
    $.ajax({
        url:'/user/login',
        type:'post',
        data:JSON.stringify({"username":$uname.val(),"password":$pwd.val()}),
        dataType:'json',
        contentType:'application/json',
        success:function(res){
            $("#btn").removeAttr('disabled')
            console.log(res);
            if(res['code']=='20'){
                // alert(res['msg']);

                $(location).attr('href','/index')
            }else{
                var a =alert(res['msg']);
                window.location.reload()
            }
        },
        beforeSend:function(){
            $("#btn_login").attr('disabled','disabled')
        }
    })

    
})