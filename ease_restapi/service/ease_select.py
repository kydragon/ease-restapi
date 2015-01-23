#!/usr/bin/python
# -*- coding: utf-8 -*-

"""ring info user system local code.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/22'

from .. import config
from .base import get, build_query_url  # build_query_string


def select_users(auth, ql=None):
    u"""获取IM用户[条件查询].

        :param auth: 身份认证
        :param ql: sql

        条件查询通过ql类实现 类似RDB的sql语句.
        比如说查询username为kylin的用户.
        查询语句就是：ql=select * where username=’kylin’.
        查询语句需要做urlencode成：select%20%2A%20where%20username%3D%27kylin%27.

        Path : /{org_name}/{app_name}/users
        HTTP Method : GET
        URL Params ：ql=select * where username=’kylin’
        Request Headers : {“Authorization”:”Bearer ${token}”}
        Request Body ： 无
        Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    """

    url = "%s/%s/%s/users" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME)

    # url = ''.join((url, build_query_string(ql)))

    # 处理数据的另外方式
    if ql:
        query = {"ql": ql}
        url = build_query_url(url, query)

    return get(url, auth)
