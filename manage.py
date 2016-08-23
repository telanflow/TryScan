#!/usr/bin/env python
#-*- coding:utf-8 -*-
import time, math
from tryscan import app, db
from tryscan.models import TaskQueue
from flask_script import Manager

__author__ = 'try'

manage = Manager(app)

@manage.command
def create_all():
    '''
    创建数据表
    :return:
    '''
    db.create_all()


@manage.command
def test():
    list = TaskQueue.query.order_by(TaskQueue.id.desc()).all()
    [print(x.id) for x in list]


if __name__ == '__main__':
    manage.run()
