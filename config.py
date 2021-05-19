#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Config File
author try
'''

DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = True

# 数据库配置：数据库用户名，数据库密码，数据库IP，端口，库名
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s' % ('root', 'root', '127.0.0.1', '3306', 'tryscan')

PAGE_SIZE = 20


# sqlmap api 服务列表
API_SERVER_LIST = [
    ['127.0.0.1', 8775]
]