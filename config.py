#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/20'

import os.path

# import sys
#
# sys.path.append('..')

from .common import get_json_path, get_json_config

APP_BASE_PATH = os.path.abspath(__file__)

# 读取外部定义配置信息:
qqland_config = get_json_config(get_json_path(APP_BASE_PATH, "info.json"))

# ORG管理员信息:
ORG_ADMIN = qqland_config[0]

org_admin_username = ORG_ADMIN['org_admin_username']
org_admin_password = ORG_ADMIN['org_admin_password']

# APP管理员信息：
APP_ADMIN = qqland_config[1]

app_admin_username = APP_ADMIN['app_admin_username']
app_admin_password = APP_ADMIN['app_admin_password']

# APP配置信息：
APP_INFO = qqland_config[2]

APP_KEY = APP_INFO['app_key']
APP_ORG = APP_INFO['app_org']
APP_NAME = APP_INFO['app_name']

CLIENT_ID = APP_INFO['client_id']
CLIENT_SECRET = APP_INFO['client_secret']

# 开放注册还是授权注册
# False: 开放注册; True: 授权注册
OPEN_OR_CREDIT = True

# 本地业务是否集成该接入
# False: 不接入; True: 接入
SWITCH_JOIN_LOCAL = False

if __name__ == '__main__':
    u"""单元测试
    """

    file_path = get_json_path(APP_BASE_PATH, "info.json")
    print file_path

    print locals()
