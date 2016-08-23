#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'try'

import threadpool, time, json
from tryscan import app, db
from tryscan.models import TaskQueue, TaskQueueLog
from sqlmapapi.task import TaskManage

def bgThread(id):
    task = TaskQueue.query.get(id) # 获取任务

    api = TaskManage(app.config['API_SERVER_LIST'][0][0], app.config['API_SERVER_LIST'][0][1])
    try:
        task_no = api.new()
        if task_no:
            task.status = 2 # 任务创建成功
            task.task_no = task_no
            db.session.commit()
        else:
            task.status = -1 # 未扫描，服务器故障
            db.session.commit()
            return task
    except Exception as e:
        # print('SqlMapApi not running')
        print(e)
        return task

    # 设置任务参数
    options = {
        'level': 2,
        'threads': 4,
        'cookie': task.cookie,
        'method': task.method,
        'headers': task.header,
        'data': task.params,
        'agent': task.user_agent,
        'referer': task.referer
    }

    # 设置任务配置
    api.optionSet(options)

    # 开始扫描
    row = api.start({'url': task.target_url})
    if row:
        task.status = 3 # 扫描中
        db.session.commit()

        # 进入循环
        while True:
            time.sleep(6)
            status = api.status()
            if status['code'] == 1:
                res = api.data()
                if res:
                    task.payload = json.dumps(res)
                task.status = 1 # 扫描成功
            elif status['code'] == -1:
                task.status = -1 # 任务未运行

            if status['code'] in [1, -1]:
                log = api.log() # 获取扫描日志
                if log:
                    for x in log:
                        TaskLog = TaskQueueLog()
                        TaskLog.task_no = api.task_id
                        TaskLog.uLevel = x['level']
                        TaskLog.uMessage = x['message']
                        TaskLog.uTime = x['time']
                        db.session.add(TaskLog)
                # 提交数据库
                db.session.commit()
                break
    else:
        task.status = 4 # 扫描失败
        db.session.commit()
    return task

def call(rThread, task):
    # rThread.requestID
    print('Call Back .....')

def run():
    pool = threadpool.ThreadPool(15) # 初始化线程池 控制线程数量

    while True:
        task = TaskQueue.query.filter_by(status=0).order_by(TaskQueue.create_time.asc()).first()
        print(task)

        if task:
            # Status -3未知 -2进入队列 -1任务未运行  0等待  1扫描完成 2任务创建成功 3进行中 4扫描失败
            task.status = -2
            db.session.commit() # Update

            # 进入扫描队列
            r = threadpool.makeRequests(bgThread, (task.id,), call)
            [pool.putRequest(req) for req in r]
        else:
            pool.wait() # 开始执行线程
            db.session.remove()
            time.sleep(5)

if __name__ == '__main__':
    run()