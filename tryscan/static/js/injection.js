$(document).ready(function(){

    $('.btn-view').click(function(){
        var self = $(this),
            task_id = Number($(this).data('id'));

        if(task_id)
        {
            self.text('加载中..');
            self.attr('disabled', 'disabled');

            $.ajax({
                url:'/task/payload',
                type:'post',
                dataType:'json',
                data:{id:task_id}
            }).done(function(res)
            {
                if(res.status == 1)
                {
                    $('.span-method').text(res.method);
                    $('input[name="url"]').val(res.url);
                    $('input[name="referer"]').val(res.referer);
                    $('input[name="user_agent"]').val(res.user_agent);
                    $('input[name="params"]').val(res.params);
                    $('textarea[name="cookie"]').val(res.cookie);

                    // headers
                    var headerItem = [];
                    for(var x in res.header){
                        headerItem.push( x + ': ' + res.header[x] + ';' );
                    }
                    $('textarea[name="header"]').val(headerItem.join('\n'));

                    // Payload
                    var payload = [];
                    for(var i in res.payload)
                    {
                        var childPayload = [],
                            item = res.payload[i];
                        childPayload.push('<div class="row"><div class="col-xs-12">');
                        childPayload.push('<div class="panel panel-primary">');
                        childPayload.push('<div class="panel-heading">注入参数：' + item.parameter + '  注入类型：' + item.place + '</div>');
                        childPayload.push('<div class="panel-body">');

                        // 注入形式
                        childPayload.push('<span class="label label-danger">参数名称：' + item.parameter + '</span>  ');
                        childPayload.push('<span class="label label-warning">注入形式：' + item.place + '</span>  ');
                        childPayload.push('<span class="label label-default">注入格式：' + item.suffix + '</span><br>');
                        childPayload.push('<span class="label label-info">测试字符：' + item.prefix + '</span>  ');
                        childPayload.push('<span class="label label-primary">数据库类型：' + item.dbms + '</span>  ');
                        childPayload.push('<span class="label label-info">数据库版本：' + item.dbms_version + '</span>  ');
                        childPayload.push('<span class="label label-primary">操作系统：' + item.os + '</span><br><br>');

                        for(var k in item.data){ // 循环单个元素的属性
                            var childData = item.data[k];
                            var cPanel = [];
                            cPanel.push('<div class="row">');
                            cPanel.push('<div class="col-xs-12">');
                            //cPanel.push('<div class="panel panel-default">');
                            //cPanel.push('<div class="panel-body">');
                            cPanel.push('<pre>');
                            cPanel.push('<span class="label label-primary">Title：' + childData.title + '</span><br>');
                            cPanel.push('<span class="label label-info">Vector：' + childData.vector + '</span><br>');
                            cPanel.push('<span class="label label-default">Where：' + childData.where + '</span><br>');
                            cPanel.push('<textarea class="form-control input-sm" style="width: 100%; height: 150px;">' + childData.payload + '</textarea>');
                            //cPanel.push('</div>');
                            cPanel.push('</pre>');
                            cPanel.push('</div>');
                            cPanel.push('</div>');

                            childPayload.push(cPanel.join(''));
                        }

                        childPayload.push('</div>'); // panel-body | End
                        childPayload.push('</div>'); // panel || End
                        childPayload.push('</div>'); // col-xs-12
                        childPayload.push('</div>'); // row

                        payload.push(childPayload.join(''));
                    }
                    $('#payload-panel').html(payload.join(''));

                    $('#modal-view').modal('show');
                }else{
                    layer.msg(res.msg);
                }

                self.text('查看详情');
                self.removeAttr('disabled');
            });
        }else{
            layer.msg('您的操作发生不可预知的错误！');
        }
    });

});