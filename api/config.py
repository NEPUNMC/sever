#!/usr/bin/python
# -*- coding:utf-8 -*-:
'''
@author: qkyzs
@license: (C) Copyright 2017-2018, Node Supply Chain Manager Corporation Limited.
@contact: nepu1960@yeah.net
@file: wechat_get.py
@time: 2019/1/26 23:17
@desc:
'''
class shuju():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:zhmsn5211314@gz-cdb-cvu5k1dx.sql.tencentcdb.com:61592/nepu'

    @staticmethod
    def init_app(app):
        pass