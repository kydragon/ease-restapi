#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""local and ring-info code integration.
"""

__author__ = 'kylin'
__date__ = '2014/09/20'

import six
import json
import random
from string import ascii_uppercase, digits
import os.path

from django.http import HttpResponse

if six.PY3:
    range_ = range
else:
    range_ = xrange


def duct_json(dict_data):
    u"""封装json返回数据.

        :param dict_data
    """

    return HttpResponse(json.dumps(dict_data, ensure_ascii=False))


def parse_app_key(app_key):
    u"""解析app_key得到org和app.

        :param app_key的规则是{org}#{app}
    """
    return tuple(app_key.split('#'))


def id_generator(size=6, chars=''.join((ascii_uppercase, digits))):
    u"""用来随机生成用户名, 仅仅用来测试用的.

        :param size: 长度
        :param chars: 限定字符
    """
    return ''.join(random.choice(chars) for _ in range_(size))


def get_json_path(base_path, conf_file=None, *path):
    u"""获取json配置文件路径.

        :param base_path: 起始点相对路径
        :param conf_file: json配置文件/其它文件
        :param path: 其它配置文件

        支持两种调用格式：
        get_json_path(base_path,conf_file)
        get_json_path(base_path,*path)
    """

    res_path = os.path.dirname(base_path)

    if conf_file:
        res_path = os.path.join(res_path, conf_file)
    else:
        res_path = os.path.join(res_path, *path)

    return res_path


def get_json_config(file_path):
    u"""从配置文件获取配置信息.

        :param file_path: json配置文件/其它文件
    """

    try:
        conf_file = open(file_path)
        json_value = json.load(conf_file)
        conf_file.close()
    except (IOError, Exception) as e:
        six.print_(e)
        return

    app_key = json_value['key']
    app_org, app_name = parse_app_key(app_key)

    org_admin_username = json_value['admin']['username']
    org_admin_password = json_value['admin']['password']

    app_admin_username = json_value['app']['admin']['username']
    app_admin_password = json_value['app']['admin']['password']

    client_id = json_value['app']['credentials']['client_id']
    client_secret = json_value['app']['credentials']['client_secret']

    org_admin = {'org_admin_username': org_admin_username, 'org_admin_password': org_admin_password}
    app_admin = {'app_admin_username': app_admin_username, 'app_admin_password': app_admin_password}

    app_info = {'app_key': app_key, 'app_name': app_name, 'app_org': app_org,
                'client_id': client_id, 'client_secret': client_secret}

    return org_admin, app_admin, app_info
