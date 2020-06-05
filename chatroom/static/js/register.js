var $uname=$("#username")
var $pwd=$("#password")
var $rpwd=$("#re_password")
var $telnumber=$("#telnumber")
var $msg=$("#uname_msg")
var $rpmsg=$("#rpwd_msg")
var $pmsg=$("#pwd_msg")
var $tmsg=$("#tel_msg")
var result=false;
function check_uname(){
    $.ajax({
        url:'/user/register/check',
        type:'post',
        async:false,
        contentType:'application/json',
        data:JSON.stringify({'uname':$uname.val()}),
        dataType:'json',
        success:function(res){
            console.log(res);
            $msg.html(res['msg']);
            if(res['code']==20){
                $msg.css("color","green");
                result = true;
            }else{
                $msg.css("color","red");
                result = false;
            }
        }
    })
}
$uname.blur(function(){
    if($uname.val()!=''){
        check_uname();
    }else{
        $msg.css("color","red");
        $msg.html('请输入用户名')
    }
})
$('#telnumber').blur(function(){
    if(check_telnumber()){
        $("#tel_msg").html('手机号无误').css('color','green')
    }else{
        $("#tel_msg").html('手机号无效').css('color','red')
        
    }
})
function check_telnumber(){
    tel=$('#telnumber').val();
    if(tel){
        $.ajax({
            type: "get",
            url: 'http://tcc.taobao.com/cc/json/mobile_tel_segment.htm?tel='+tel,
            dataType: "jsonp",
            jsonp: "callback",
            success: function(data){
            console.log(data);
            if(data.province){
                return true
            }else{
                return false
            }
            },
            error:function (e){    
            console.log(e)      
            }
        });
    }
   
}
$("#btn_register").click(function(){
    

    if($uname.val()==''){
        $msg.html('用户名不可为空').css('color','red');
        if($pwd.val()==''){
            $pmsg.html('密码不可为空').css('color','red');
        }
        if($rpwd.val()==''){
            $rpmsg.html('请再输入一次密码').css('color','red');
        }
    }
    else if(!result){
        alert('请重新输入用户名');
        $msg.html('请重新输入用户名').css('color','red');
        $uname.val('');
    }else if (!check_telnumber()){
        alert('请重新输入用户名');
    }
    else{
        console.log(result)
        $.ajax({
            url:'/user/register',
            type:'post',
            data:JSON.stringify({"dur":1,'uname':$uname.val(),'password':$pwd.val(),'repassword':$rpwd.val(),'telnumber':$telnumber.val()}),
            dataType:'json',
            contentType:'application/json',
            async:true,
            success:function(res){
                alert(res['msg']);
                $(location).attr('href','/index');
            }
        })

    }
})

$rpwd.blur(function (){
    if($pwd.val()!=''&&$rpwd.val()!=''){
        if($pwd.val()==$rpwd.val()){
            $rpmsg.css('color','green')
            $rpmsg.html('两次密码输入一致')
        }else{
            $rpmsg.css('color','red')
            $rpmsg.html('两次密码输入不一致')
        }
    }
})
$pwd.blur(function(){
    if($pwd.val()!=''&&$rpwd.val()!=''){
        if($pwd.val()==$rpwd.val()){
            $rpmsg.css('color','green')
            $rpmsg.html('两次密码输入一致')
        }else{
            $rpmsg.css('color','red')
            $rpmsg.html('两次密码输入不一致')
        }
    }
})
