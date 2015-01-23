#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ring info remote api interface base.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/20'

import os
import time
import json
import random
import os.path
import requests

import six


if six.PY3:
    from urllib.parse import urlencode, quote
else:
    from urllib import urlencode, quote

from .. import config


def check_file_dir(dir_path):
    u"""检查目录是否存在, 若不存在创建.

        :param dir_path: 目录
    """

    os.path.isdir(dir_path)

    def create_path(my_path):
        u"""创建目录

            :param my_path: 目录
        """

        if not os.path.exists(my_path):
            os.mkdir(my_path)

        if os.path.exists(my_path):
            return my_path
        else:
            return create_path(my_path)

    if config.DIR_DOWNLOAD_FILES:
        return create_path(config.DIR_DOWNLOAD_FILES)
    else:
        return create_path(dir_path)


def build_file_rename(file_name):
    u"""本地文件上传异地重命名

        :param file_name: 文件名
    """

    str_file_suf = file_name.split('.')[-1]
    str_time_rnd = '_'.join((str(int(time.time())), str(random.randint(10000, 99999))))

    return '.'.join((str_time_rnd, str_file_suf))


def build_query_url(url, dict_data):
    u"""构建get形式的请求地址

        :param url: 请求地址
        :param dict_data:dict形式的query数据
    """

    # urlencode() 不幸的是, 这个函数只能接收key-value pair格式的数据, 即只针对dict的.
    params = urlencode(dict_data)
    return "%s?%s" % (url, params)


def build_query_string(ql=None):
    u"""构建sql query 的查询urlencode

        :param ql: sql
    """

    result = ''

    if ql:
        result = "?ql=%s" % quote(ql)
        # result = "?" + "ql=%s" % unquote(ql)
        # result = "?" + "ql=%s" % base64.urlsafe_b64encode(ql)  # urlsafe_b64encode 接不上REST API

    return result


def check_ring_id(ring_id):
    u"""检测环信ID.

        :param ring_id: 环信账户名

        环信ID需要使用英文字母和（或）数字的组合
        环信ID不能使用中文
        环信ID不能使用email地址
        环信ID不能使用UUID
        环信ID中间不能有空格或者井号（#）等特殊字符
    """

    six.print_(str(ring_id))

    pass


def put(url, payload, auth=None):
    u"""构建put请求

        :param url: 请求地址
        :param payload:　dict形式的query数据
        :param auth: 身份认证
    """
    r = requests.put(url, data=json.dumps(payload), headers=config.JSON_HEADER, auth=auth)
    return http_result(r)


def post(url, payload, auth=None):
    u"""构建Post请求

        :param url: 请求地址
        :param payload:　dict形式的query数据
        :param auth: 身份认证
    """
    r = requests.post(url, data=json.dumps(payload), headers=config.JSON_HEADER, auth=auth)
    return http_result(r)


def get(url, auth=None):
    u"""构建Get请求

        :param url: 请求地址
        :param auth: 身份认证
    """

    r = requests.get(url, headers=config.JSON_HEADER, auth=auth)
    return http_result(r)


def delete(url, auth=None):
    u"""构建Delete请求.

        :param url: 请求地址
        :param auth: 身份认证
    """
    r = requests.delete(url, headers=config.JSON_HEADER, auth=auth)
    return http_result(r)


def http_result(r):
    u"""解析返回结果.

        :param r: 返回对象
    """

    if config.REST_API_DEBUG:
        error_log = {
            "method": r.request.method,
            "url": r.request.url,
            "request_header": dict(r.request.headers),
            "response_header": dict(r.headers),
            "response": r.text
        }
        if r.request.body:
            error_log["payload"] = r.request.body
            # six.print_(json.dumps(error_log)

    if r.status_code == requests.codes.ok:
        return True, r.json()
    else:
        return False, r.text
