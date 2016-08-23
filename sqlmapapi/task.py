#!/usr/bin/env python
#-*- coding:utf-8 -*-
import requests, json

__author__ = 'Try'

class TaskManage():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.address = 'http://' + self.host + ':' + str(self.port)
    def setTaskId(self, task_id=''):
        self.task_id = task_id

    def new(self):
        '''
        创建新的任务
        :return: 任务ID
        '''
        url = self.address + '/task/new'
        response = json.loads(requests.get(url).text)
        if response['success'] == True:
            self.task_id = response['taskid']
            return self.task_id
        else:
            return False

    def delete(self, task_id=''):
        '''
        删除任务
        :param task_id: SqlMap任务ID 可空
        :return: Boolean
        '''
        if task_id == '':
            task_id = self.task_id
        url = self.address + '/task/' + task_id + '/delete'
        response = json.loads(requests.get(url).text)
        if response['success'] == True:
            return True
        else:
            return False

    def optionList(self, task_id=''):
        '''
        获取所有配置信息
        :param task_id: SqlMap任务ID 可空
        :return: Dict
        '''
        if task_id == '':
            task_id = self.task_id
        url = self.address + '/option/' + task_id + '/list'
        response = json.loads(requests.get(url).text)
        if response['success'] == True:
            return response['options']
        else:
            return False

    def optionGet(self, task_id=''):
        '''
        获取任务的配置信息
        :param task_id: SqlMap任务ID 可空
        :return: Boolean
        '''
        if task_id == '':
            task_id = self.task_id
        url = self.address + '/option/' + task_id + '/get'
        response = json.loads(requests.post(url).text)
        if response['success'] == True:
            return response
        else:
            return False

    def optionSet(self, options, task_id=''):
        '''
        设置任务配置信息
        :param options: JSON对象
        :param task_id: SqlMap任务ID 可空
        :return: Boolean
        '''
        if task_id == '':
            task_id = self.task_id
        url = self.address + '/option/' + task_id + '/set'
        response = json.loads(requests.post(url, data=json.dumps(options), headers={'Content-Type': 'application/json'}).text)
        if response['success'] == True:
            return True
        else:
            return False

    def start(self, option, task_id=''):
        '''
        启动扫描任务
        :param option: 设置 {'url': '目标地址', 'cookie': '', 'agent': '', ... }
        :param task_id: SqlMap任务ID 可空
        :return: Boolean || ID
        '''
        if task_id == '':
            task_id = self.task_id
        url = self.address + '/scan/' + task_id + '/start'
        response = json.loads(requests.post(url, data=json.dumps(option), headers={'Content-Type': 'application/json'}).text)
        if response['success'] == True:
            return response['engineid'] # 返回引擎ID
        else:
            return False

    def stop(self, task_id=''):
        '''
        停止扫描任务
        :param task_id: SqlMap任务ID 可空
        :return: Boolean
        '''
        if task_id == '':
            task_id = self.task_id
        url = self.address + '/scan/' + task_id + '/stop'
        response = json.loads(requests.get(url).text)
        if response['success'] == True:
            return True
        else:
            return False

    def log(self, start=-1, end=-1, task_id=''):
        '''
        打印扫描任务日志信息
        :param start: 开始的记录数 可空（用于分页）
        :param end: 结束的记录数 可空（用于分页）
        :param task_id: SqlMap任务ID 可空
        :return: False || [ {message:'', level:'INFO|WARNING', time:'14:11:23'}, {}, ... ]
        '''
        if task_id == '':
            task_id = self.task_id
        url = self.address + '/scan/' + task_id + '/log'
        if start > -1 and end > -1:
            url += '/' + start + '/' + end
        response = json.loads(requests.get(url).text)
        if response['success'] == True:
            return response['log']
        else:
            return False

    def kill(self, task_id=''):
        '''
        终结扫描任务的进程
        :param task_id: SqlMap任务ID 可空
        :return: Boolean
        '''
        if task_id == '':
            task_id = self.task_id
        url = self.address + '/scan/' + task_id + '/kill'
        response = json.loads(requests.get(url).text)
        if response['success'] == True:
            return True
        else:
            return False

    def status(self, task_id=''):
        '''
        获取任务的状态
        :param task_id: SqlMap任务ID 可空
        :return: {'code':0, 'msg':''}   terminated=结束
        '''
        if task_id == '':
            task_id = self.task_id
        url = self.address + '/scan/' + task_id + '/status'
        response = json.loads(requests.get(url).text)

        ret = {'code':-3, 'msg':'未知错误'}
        if response['success'] == True:
            ret['msg'] = response['status']
            if response['status'] == 'not running':
                ret['code'] = -1 # 未运行任务
            elif response['status'] == 'terminated':
                ret['code'] = 1 # 扫描完成
            elif response['status'] == 'running':
                ret['code'] = 2 # 进行中
            else:
                ret['code'] = -3 # 未知
        return ret

    def data(self, task_id=''):
        '''
        检索扫描的数据
        :param task_id: SqlMap任务ID 可空
        :return:
        '''
        if task_id == '':
            task_id = self.task_id
        url = self.address + '/scan/' + task_id + '/data'
        response = json.loads(requests.get(url, headers={'Content-Type': 'application/json'}).text)
        if response['success'] == True:
            ret = []
            for i in response['data']:
                values = i['value']
                for v in values:
                    item = {}
                    item['clause'] = v['clause']
                    item['dbms'] = v['dbms'] # 目标数据库类型  Mysql Oracle Sqlite sql_server
                    item['dbms_version'] = v['dbms'] # 目标数据库版本
                    item['os'] = v['os'] # 目标系统
                    item['parameter'] = v['parameter'] # 注入参数
                    item['place'] = v['place'] # 注入位置 :Cookie
                    item['prefix'] = v['prefix'] # 注入的前缀  类似： '
                    item['ptype'] = v['ptype']
                    item['suffix'] = v['suffix'] # 注入语句格式  类似： AND '[RANDSTR]'='[RANDSTR]

                    item['data'] = []
                    if v['data']:
                        params = v['data']
                        for d in params:
                            childParams = {
                                'title': params[d]['title'],
                                'payload': params[d]['payload'],
                                'vector': params[d]['vector'],
                                'where': params[d]['where']
                            }
                            item['data'].append(childParams)
                    ret.append(item)
            return ret
        else:
            return []

    def getTaskList(self, admin_id=''):
        '''
        获取任务列表
        :param admin_id:
        :return: {"tasks": {"5f6ee4dd994c18db": "terminated", "988c2bb3ea4e61f6": "not running"}, "tasks_num": 2, "success": true}
        '''
        url = self.address + '/admin/' + admin_id + '/list'
        response = json.loads(requests.get(url).text)
        if response['success'] == True:
            return response
        else:
            return False
if __name__ == '__main__':
    task = TaskManage()
    print(task.new())