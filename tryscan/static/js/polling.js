$(document).ready(function(){



    // 定时获取服务器状态
    //setInterval(getServerStatus, 3000);

    // 获取任务信息
    setInterval(getServerTaskInfo, 3000);

    // 获取任务状态
    setInterval(getTaskStatus, 5000);
});

// 获取服务器内存信息
function getServerStatus()
{
    $.ajax({
        url:'/server/info',
        dataType:'json',
        type:'post',
        success:function(res)
        {
            if(res.status == 1){
                v = res.use / res.total * 100;
                $('#server_info').width(v + '%');
            }
        }
    })
}

// 获取服务器任务信息
function getServerTaskInfo()
{
    $.ajax({
        url:'/server/task_info',
        dataType:'json',
        type:'post',
        success:function(res)
        {
            if(res.status == 1){
                vConduct = res.conduct / res.total * 100;
                vComplete = res.complete / res.total * 100;
                $('#task_conduct').width(vConduct+'%');
                $('#task_complete').width(vComplete+'%');
            }
        }
    })
}

function getTaskStatus()
{
    var aId = [];
    $('.task_id').each(function(){
        // 只要状态不为1的时候 才会获取
        if($(this).data('status') == 1){
            var id = Number($(this).text());
            aId.push(id);
        }
    });
    var ids = aId.join(',');

    if(ids)
    {
        $.ajax({
            url:'/task/status',
            type:'post',
            data:{ids:ids},
            dataType:'json',
            success:function(res)
            {
                if(res.status == 1){
                    var list = res.data;

                    for(var x in list)
                    {
                        var span = '';
                        switch(list[x].status)
                        {
                            case 0:
                                span = '<span class="label label-default">等待</span>';break;
                            case 1:
                                span = '<span class="label label-success">扫描完成</span>';break;
                            case 2:
                                span = '<span class="label label-info">任务创建成功</span>';break;
                            case 3:
                                span = '<span class="label label-primary">扫描中</span>';break;
                            case 4:
                                span = '<span class="label label-danger">扫描失败</span>';break;
                            case -1:
                                span = '<span class="label label-warning">任务未运行</span>';break;
                            case -2:
                                span = '<span class="label label-info">进入队列</span>';break;
                            default:
                                break;
                        }

                        $('#task_'+ list[x].id).html(span);
                        if(list[x].status == 1){
                            $('#task_'+ list[x].id).parent().find('td').eq(0).data('status', 0);
                        }
                    }

                }
            }
        });
    }
}