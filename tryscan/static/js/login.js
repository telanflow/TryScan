$(document).ready(function(){

    layer.config({offset: 0});

    $('#btn-login').click(function(){
        var client_id = $.trim($('#client_id').val());
        if(client_id)
        {
            var params = {
                client_id: client_id
            };

            $.ajax({
                url:'/login',
                data: params,
                type:'post',
                dataType:'json',
                success:function(res)
                {
                    if(res.status == 1){
                        layer.msg('设置成功，即将进入~');
                        setTimeout(function(){
                            window.location.href = '/list';
                        }, 1500);
                    }else{
                        layer.msg('Client_ID 有误，请重新输入！');
                    }
                }
            })

        }else{
            layer.msg('请输入你的Client_ID');
        }

    })

});