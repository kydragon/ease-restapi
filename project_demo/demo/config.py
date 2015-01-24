#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""config data.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/20'

from ease_restapi import config

# ORG管理员信息:
ORG_ADMIN_USERNAME = "kylinfish"
ORG_ADMIN_PASSWORD = "kylin123456"

config.ORG_ADMIN_USERNAME = ORG_ADMIN_USERNAME
config.ORG_ADMIN_PASSWORD = ORG_ADMIN_PASSWORD

# APP管理员信息：
APP_ADMIN_USERNAME = 'kylin'
APP_ADMIN_PASSWORD = 'hello666'

config.APP_ADMIN_USERNAME = APP_ADMIN_USERNAME
config.APP_ADMIN_PASSWORD = APP_ADMIN_PASSWORD

# APP配置信息：
APP_KEY = 'kylin9999#demo'
APP_ORG = 'kylin9999'

APP_NAME = 'demo'
CLIENT_ID = 'YXA66mgIMKMTEeS2e530rkCQUA'
CLIENT_SECRET = 'YXA6fAHitxx_DueYiHIgxTQxhIW_DXY'

config.APP_KEY = APP_KEY
config.APP_ORG = APP_ORG
config.APP_NAME = APP_NAME

config.CLIENT_ID = CLIENT_ID
config.CLIENT_SECRET = CLIENT_SECRET

# APP download storage:
DIR_DOWNLOAD_FILES = ''
config.DIR_DOWNLOAD_FILES = DIR_DOWNLOAD_FILES

# APP admin token expires time:
EXPIRES_IN = None  # 秒为单位, None为默认值. 官方默认是七天, 在有效期内不需要重复获取, 7天*24时*60分*60秒.
config.EXPIRES_IN = EXPIRES_IN

# 开放注册还是授权注册
# False: 开放注册; True: 授权注册
OPEN_OR_CREDIT = True
config.OPEN_OR_CREDIT = OPEN_OR_CREDIT

# 本地业务是否集成该接入
# False: 不接入; True: 接入
SWITCH_JOIN_LOCAL = True
config.SWITCH_JOIN_LOCAL = SWITCH_JOIN_LOCAL
