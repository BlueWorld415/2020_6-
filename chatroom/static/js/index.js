$("#new_room").hide()
var data_obj=null
$(document).ready(get_room_list());
var num=0;
var content_list=[];
var room_list=[];
var username=null;
function get_room_list() {
    $.ajax({
        url:'/room',
        type:'get',
        dataType:'json',
        success:function(data){
            console.log(data);
            // console.log(JSON.parse( data['data']));
            if(data['code']==41){
                console.log('没有聊天室')
                console.log(data['data'])
            }else if(data['code']==20){
                data_obj=data['data'];
                console.log(data_obj)
                username=data['user'];
                $("#uname").html(username);
                $.each(data_obj,function(i,e){
                    var room=$("<div class='room'><span id='room_name'>"+e.roomname+"</span><br>"+
                        "<div class='owner'>" +
                        "<span id='own'>聊天室管理员:</span>" +
                        "<span id='owner_id'>"+e.owner+"</span>" +
                        "</div></div>");
                    room_list.push(room);
                    $("#left").append(room);
                    var content=$("<div id='content'><div id='introduce_name'>" +
                            "<div id='irn'>" + e.roomname +
                            "</div><p id='room_id' style='display:none;'>"+e.id+"</p>" +
                            "<div id='iro'>" +
                            "聊天室管理员：" +
                            "</div>" +"<div id='iron'>" +e.owner+
                            "</div>"+
                            "</div>" +
                            "<div id='introduce'>" +
                            "<div id='in'>聊天室简介</div>" +
                            "<div id='ic'>"+e.introduce+"</div>" +
                            "</div></div>"+"<button id='in_btn' class='btn btn-block btn-info' onclick='in_room()'>进入聊天室</button>")
                    content_list.push(content);
                   
                })
                
                $(".room").click(function() {
                    for (var i=0;i<room_list.length;i++){
                        if(this==room_list[i][0]){
                            console.log(i);
                            num=i;
                            
                            console.log(num);
                        }
                    }
                    $("#right").html(content_list[num]);
                })

            }else if(data['code']==40){
                console.log('未登录');
                console.log(data['data']);
                $(location).attr('href','/user/login')
            }
        }
    })

    
}

$("#logout").click(function(){
    $.get('/user/logout',function(res){
        if(res['code']=='20'){
            location.reload();
        }
    },'json');
})

$("#btn_new").click(function(){
    $("#new_room").fadeIn(100)
    $("#main").fadeOut(100)
})
$("#n_btn").click(function(){
    r_name=$("#r_name")
    r_intr=$("#r_intro")
    $.ajax({
        url:'/room',
        type:'post',
        dataType:'json',
        contentType:"application/json",
        data:JSON.stringify({r_name:r_name.val(),r_intro:r_intr.val()}),
        success:function(res){
            if (res.code=='21'){
                location.reload();
            }else if (res.code=='43'){
                alert('聊天室名称不可重复');
                location.reload();
            }else {
                console.log('预料之外的错误');
                console.log(res);
            }
        }
    })
    
    
})

function in_room(){
    rname=$("#irn").html()
    // console.log($("#room_id").html());
    window.location.href='/chat?rname='+rname
}
$("#modify").hide()
$("#btn_modify").click(function(){
    $("#main").fadeOut(100)
    $("#modify").fadeIn(100)
})
$('#modify_btn').click(function(){
    $.ajax({
        url:'/user/modify',
        type:'post',
        dataType:'json',
        data:JSON.stringify({username:$('#n_name').val(),password:$("#n_pass").val(),repassword:$("#rn_pass").val(),tel:$("#n_tel").val()}),
        contentType:"application/json",
        success:function(res){
            console.log(res);
            if(res['code']==200){
                console.log('yes')
                $("#msg").html('修改成功').css('color','green')
                location.reload()
            }
        }
    })
})
$(".cancel").click(function(){
    $("#modify").fadeOut(100)
    $("#new_room").fadeOut(100)
    $("#main").fadeIn(100)
})