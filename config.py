#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Config File
author try
'''

DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s' % ('root', '', '127.0.0.1', '3306', 'test')

PAGE_SIZE = 20


# SqlMap多服务列表
API_SERVER_LIST = [
    ['s.try255.com', 7789]
]