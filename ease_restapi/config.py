#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""config data.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/20'


# ORG管理员信息:
ORG_ADMIN_USERNAME = ''
ORG_ADMIN_PASSWORD = ''

# APP管理员信息：
APP_ADMIN_USERNAME = ''
APP_ADMIN_PASSWORD = ''

# APP配置信息：
APP_KEY = ''
APP_ORG = ''
APP_NAME = ''

CLIENT_ID = ''
CLIENT_SECRET = ''

# APP download storage:
DIR_DOWNLOAD_FILES = ''

# APP admin token expires time:
EXPIRES_IN = None  # 秒为单位, None为默认值. 官方默认是七天, 在有效期内不需要重复获取, 7天*24时*60分*60秒.

JSON_HEADER = {'content-type': 'application/json'}
HOST_SERVER = 'https://a1.easemob.com'

REST_API_DEBUG = True

# 开放注册还是授权注册
# False: 开放注册; True: 授权注册
OPEN_OR_CREDIT = True

# 本地业务是否集成该接入
# False: 不接入; True: 接入
SWITCH_JOIN_LOCAL = True
