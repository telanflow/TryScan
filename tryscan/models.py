#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time, math
from tryscan import db
from flask_login import UserMixin


__author__ = 'try'

# DB_LINK = 'mysql://%s:%s@%s:%d/%s' % app.config['DB_CONFIG']['user'], app.config['DB_CONFIG']['password'], app.config['DB_CONFIG']['host'], app.config['DB_CONFIG']['port'], app.config['DB_CONFIG']['name']

class TaskQueue(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    __tablename__ = 'ts_task_queue'
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_no   = db.Column(db.CHAR(10), default='', index=True, nullable=False, server_default='')
    domain      = db.Column(db.VARCHAR(35), index=True, nullable=False)
    method      = db.Column(db.VARCHAR(8), default='GET', nullable=False, server_default='GET')
    target_url  = db.Column(db.VARCHAR(500), nullable=False, index=True)
    params      = db.Column(db.VARCHAR(2000), default='', nullable=False, server_default='')
    header      = db.Column(db.TEXT, default='')
    cookie      = db.Column(db.TEXT, default='')
    user_agent  = db.Column(db.VARCHAR(350), default='', server_default='', nullable=False)
    referer     = db.Column(db.VARCHAR(500), default='', server_default='', nullable=False)
    task_no     = db.Column(db.CHAR(16), default='', server_default='', nullable=False, index=True)
    payload     = db.Column(db.TEXT, default='')
    modify_time = db.Column(db.Integer, default=math.floor(time.time()), nullable=False, server_onupdate=str(math.floor(time.time())))
    create_time = db.Column(db.Integer, default=math.floor(time.time()), nullable=False)
    status      = db.Column(db.SMALLINT, default=0, index=True, nullable=False, server_default='0')
    def __init__(self):
        pass
    def __repr__(self):
        return '<ClientNo %r>' % self.client_no
    def __str__(self):
        return '<ID %r>' % self.id

class TaskQueueLog(db.Model):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    __tablename__ = 'ts_task_queue_log'
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_no     = db.Column(db.CHAR(16), index=True, nullable=False)
    uLevel      = db.Column(db.VARCHAR(15), default='', server_default='', nullable=False)
    uMessage    = db.Column(db.TEXT, default='')
    uTime       = db.Column(db.VARCHAR(15), default='', server_default='', nullable=False)
    create_time = db.Column(db.Integer, default=math.floor(time.time()), server_default='0', nullable=False)

class User(UserMixin):
    def __init__(self, client_id):
        self.client_id = client_id
    def get_id(self):
        return self.client_id