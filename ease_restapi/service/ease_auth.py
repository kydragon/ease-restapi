#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
获取APP管理员Token
环信提供的REST API需要权限才能访问, 权限通过发送HTTP请求时携带token来体现, 下面描述获取token的方式.
小说明: api描述的时候使用到app的{client_id}或者{app管理员密码}之类的这种参数需要替换成具体的值.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/24'

import json
import requests

from .. import config


def get_token_client():
    u"""使用app的client_id和client_secret获取授权token.

        client_id 和 client_secret可以在环信管理后台的app详情页面看到

        Path: /{org_name}/{app_name}/token
        HTTP Method: POST
        URL Params: 无
        Request Headers: {“Content-Type”:”application/json”}
        Request Body:
            {
                “grant_type”: “client_credentials”,
                ”client_id”: “{app的client_id}”,
                ”client_secret”: “{app的client_secret}”
            }

        curl -X
        POST "https://a1.easemob.com/easemob-demo/chatdemo/token"
        -d '{
            "grant_type":"client_credentials",
            "client_id":"YXA6wDs-MARqEeSO0VcBzaqg11",
            "client_secret":"YXA6JOMWlLap_YbI_ucz77j-4-mI0dd"
        }'
    """

    payload = {
        "grant_type": "client_credentials",
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET
    }

    url = "%s/%s/%s/token" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME)
    success, result = requests.post(url, data=json.dumps(payload), headers=config.JSON_HEADER)
    if success:
        return result['access_token'], result['expires_in']


def get_token_account(username, password):
    u"""使用app管理员的username和password获取授权token.

        :param username: 用户名
        :param password: 密码

        Path : /{org_name}/{app_name}/token
        HTTP Method : POST
        URL Params ： 无
        Request Headers : {“Content-Type”:”application/json”}
        Request Body ： {“grant_type”: “password”,”username”:”${app管理员用户名}”,”password”:”${app管理员密码}”}
    """

    payload = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }

    url = "%s/%s/%s/token" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME)
    success, result = requests.post(url, data=json.dumps(payload), headers=config.JSON_HEADER)
    if success:
        return result['access_token'], result['expires_in']
