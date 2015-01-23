#!/usr/bin/python
# -*- coding: utf-8 -*-

"""ring info user system local code.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/22'

# import base64

from .. import config
from .base import get, post, delete, build_query_url


def create_users(auth, play_load):
    u"""注册IM用户[批量] 建议批量不要过多, 在20-60之间.

        :param auth: 身份认证
        :param play_load: [{'username':'${用户名1}','password':'${密码}'},…]

        Path : /{org_name}/{app_name}/users
        HTTP Method : POST
        URL Params ： 无
        Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
        Request Body ： [{“username”:”${用户名1}”,”password”:”${密码}”},…,{“username”:”${用户名2}”,”password”:”${密码}”}]
        Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    """

    url = "%s/%s/%s/users" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME)
    return post(url, play_load, auth)


def pickup_users(auth, limit=None, cursor=None):
    u"""获取IM用户[批量查询].

    :param auth: 身份认证
    :param limit: 数量值
    :param cursor: 游标

    该接口默认返回最近创建的10个用户, 如果需要指定获取数量，需加上参数limit=N，N为数量值.
    关于分页：如果DB中的数量大于N, 返回json会携带一个字段“cursor”, 我们把它叫做”游标”, 该游标可理解为结果集的指针, 值是变化的.

    往下取数据的时候带着游标, 就可以获取到下一页的值.
    如果还有下一页, 返回值里依然还有这个字段, 直到没有这个字段, 说明已经到最后一页.
    cursor的意义在于数据(真)分页.

    1) 不分页

        Path : /{org_name}/{app_name}/users
        HTTP Method : GET
        URL Params ： limit=20
        Request Headers : {“Authorization”:”Bearer ${token}”}
        Request Body ： 无
        Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。

    2) 分页

        Path : /{org_name}/{app_name}/users
        HTTP Method : GET
        URL Params ： limit=20&cursor=LTU2ODc0MzQzOnNmdTlxdF9LRWVPaVFvMWlBZmc4S3c
        Request Headers : {“Authorization”:”Bearer ${token}”}
        Request Body ： 无
        Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    """

    url = "%s/%s/%s/users" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME)

    payload = []
    if limit:
        payload.append("limit=%d" % limit)
    if cursor:
        payload.append("cursor=%s" % cursor)

    if payload:
        url = ''.join((url, "?", "&".join(payload)))

    # 处理数据的另外方式
    # query = {"limit": limit, "cursor": cursor}
    # url = build_query_url(url, query)

    return get(url, auth)


def delete_users(auth, ql=None, limit=None):
    u""""删除IM用户[批量].

    :param auth: 身份认证
    :param ql: sql
    :param limit: 数量值

    删除某个app下指定数量的环信账号。可一次删除N个用户, 数值可以修改.
    建议这个数值在100-500之间, 不要过大.
    需要注意的是, 这里只是批量的一次性删除掉N个用户, 具体删除哪些并没有指定, 可以在返回值中查看到哪些用户被删除掉了.

    可以通过增加查询条件来做到精确的删除, 例如:

        按照创建时间来排序(降序)
            DELETE /{org_name}/{app_name}/users?ql=order+by+created+desc&limit=300

        按照创建时间来排序(升序)
            DELETE /{org_name}/{app_name}/users?ql=order+by+created+asc&limit=300

        按时间段来删除 使用ql=created> {起始时间戳} and created < {结束时间戳} 的查询语句, 时间戳是timestamp类型的, 并且需要对ql进行http url encode
            DELETE /{org_name}/{app_name}/users?ql=created > 1409506121910 and created < 1409576121910

        Path : /{org_name}/{app_name}/users
        HTTP Method : DELETE
        URL Params : limit=30
        Request Headers : {“Authorization”:”Bearer ${token}”}
        Request Body ： 无
        Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    """

    url = "%s/%s/%s/users" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME)

    """
    payload = []
    if ql:
        payload.append("ql=%s" % base64.urlsafe_b64encode(ql)) # urlsafe_b64encode 接不上REST API
    if limit:
        payload.append("limit=%d" % limit)

    if payload:
        url = ''.join((url, "?", "&".join(payload)))
    """

    # 处理数据的另外方式
    query = {"limit": limit, "ql": ql}
    url = build_query_url(url, query)

    return delete(url, auth)


def add_group_users(auth, group_id, usernames):
    u"""群组批量添加成员.

        :param auth: 身份认证
        :param group_id: 群组ID, 注意: 非群组名称
        :param usernames: 用户列表

        Path : /{org_name}/{app_name}/chatgroups/{chatgroupid}/users
        HTTP Method : POST
        URL Params ： 无
        Request Headers : {“Authorization”:”Bearer ${token}”}
        Request Body ：{“usernames”:[“username1”,”username2”]}’
                        — usernames固定属性，作为json的KEY；username1/username2 要添加到群中的成员用户名，可变

        Response Body ：详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略
    """

    payload = {"usernames": usernames}
    url = "%s/%s/%s/chatgroups/%s/users" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME, group_id)
    return post(url, payload, auth)
