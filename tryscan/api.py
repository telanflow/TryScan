#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re, json
from tryscan import app, db
from tryscan.models import TaskQueue
from flask import request, jsonify
from flask_login import login_required, current_user


@app.route('/task/add', methods=['POST'])
def CreateTask():
    '''
    添加扫描任务到数据库
    :return: json
    '''
    mData = request.values.to_dict()
    if mData:
        task = TaskQueue.query.filter_by(method=mData['method'], target_url=mData['url']).first()
        if not task:
            mTaskQueue = TaskQueue()
            mTaskQueue.client_no = mData['client_no']
            mTaskQueue.target_url = mData['url']
            mTaskQueue.header = mData['headers']
            mTaskQueue.method = mData['method']
            mTaskQueue.params = mData['data']
            mTaskQueue.cookie = mData['cookie']
            mTaskQueue.user_agent = mData['user_agent']
            mTaskQueue.referer = mData['referer']
            mTaskQueue.status = 0

            match = re.search(r'\://([\.a-zA-Z0-9]+)/?', mData['url'])
            if match:
                mTaskQueue.domain = match.groups()[0]
            else:
                mTaskQueue.domain = ''

            db.session.add(mTaskQueue)
            db.session.commit()
            return jsonify({'status':1, 'msg':'success'}), 200
        else:
            return jsonify({'status':0, 'msg':'Task Exist'}), 200
    else:
        return jsonify({'status':0, 'msg':'error'}), 200

@app.route('/task/payload', methods=['POST'])
@login_required
def GetTaskPayload():
    '''
    获取单个任务的Payload信息
    :return:
    '''
    if request.method == 'POST':
        client_no = current_user.get_id()
        task_id = request.form.get('id', False)

        if task_id and client_no:
            aTaskInfo = TaskQueue.query.filter_by(id=task_id, client_no=client_no).first()
            if aTaskInfo:
                ret = {
                    'status': 1,
                    'method': aTaskInfo.method,
                    'url': aTaskInfo.target_url,
                    'params': aTaskInfo.params,
                    'header': json.loads(aTaskInfo.header),
                    'user_agent': aTaskInfo.user_agent,
                    'referer': aTaskInfo.referer,
                    'cookie': aTaskInfo.cookie,
                    'payload': json.loads(aTaskInfo.payload)
                }
                return jsonify(ret), 200
            else:
                return jsonify({'status':0, 'msg':'当前任务不存在！'})
        else:
            return jsonify({'status':0, 'msg':'非法操作'})
    else:
        return jsonify({'status':0, 'msg':'非法操作！'}), 404

@app.route('/task/status', methods=['POST'])
@login_required
def GetTaskStatus():
    '''
    获取一组任务的状态
    :return:
    '''
    ids = request.form.get('ids', False)
    if ids:
        aIds = ids.split(',')
        client_no = current_user.get_id()

        if aIds and client_no:
            list = TaskQueue.query.filter(TaskQueue.id.in_(aIds)).filter_by(client_no=client_no).all()

            aTaskList = []
            for x in list:
                aTaskList.append({'id':x.id, 'status':x.status})

            ret = {
                'status':1,
                'data':aTaskList
            }
            return jsonify(ret), 200
        else:
            return jsonify({'status': 0, 'msg': 'Not Login'}), 200
    else:
        return jsonify({'status':0, 'msg':'Not Found Id'}), 200

@app.route('/server/info', methods=['POST'])
def ServerInfo():
    '''
    获取服务器内存使用情况
    :return: json
    '''
    try:
        with open('/proc/meminfo') as f:
            total = int(f.readline().split()[1])
            free = int(f.readline().split()[1])
            buffers = int(f.readline().split()[1])
            cache = int(f.readline().split()[1])
        mem_use = total-free-buffers-cache

        ret = {
            'status': 1,
            'total': total / 1024,
            'use': mem_use / 1024
        }
        return jsonify(ret), 200
    except Exception as e:
        return jsonify({'status':0, 'msg':'Error'}), 200

@app.route('/server/task_info', methods=['POST'])
@login_required
def ServerTaskInfo():
    '''
    获取服务器正在运行的任务数
    :return:
    '''
    client_no = current_user.get_id()
    if client_no:
        Total = TaskQueue.query.filter_by(client_no=client_no, status=1).count()
        Complete = TaskQueue.query.filter_by(client_no=client_no, status=1).count()
        Conduct = TaskQueue.query.filter_by(client_no=client_no, status=3).count()

        ret = {
            'status': 1,
            'total': Total,
            'complete': Complete,
            'conduct': Conduct
        }
        return jsonify(ret), 200
    else:
        return jsonify({'status': 0, 'msg':'Not Login'}), 200