#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ring info client service sdk.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/22'

import base64

from .. import config
from .base import get


def export_chat_message(auth, ql=None, limit=None, cursor=None):
    u"""导出聊天记录, 取聊天记录.

        :param auth: 身份认证
        :param ql:
        :param limit:
        :param cursor:

        Path : /{org_name}/{app_name}/chatmessages
        HTTP Method : GET
        URL Params ： 无
        Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
        Response Body ： 聊天记录(json),默认返回10条记录

    使用示例1：获取最新的20条记录
        在url后面加上参数ql=order by timestamp desc，limit=20,实际使用时需要对”=”后边的内容进行utf8 encode转义

    使用示例2：获取某个时间段内的消息
        在url后面加上参数ql=select * where timestamp<1403164734226 and timestamp>1403166586000 order by timestamp desc,
        同上”=”后的参数需要转义

    使用示例3：分页获取数据
        使用limit参数获取数据完毕后，如果后边还有数据，会返回一个不为空的cursor回来，使用这个cursor就能进行分页获取了。

    分页示例：根据之前获取数据返回的cursor继续获取后面的20条数据。
        在url后面加上参数
        ql=order by timestamp desc
        limit=20
        cursor=MTYxOTcyOTYyNDpnR2tBQVFNQWdHa0FCZ0ZHczBNRWVPMjdMRWo5b0w4dEFB
        同上参数需要转义
    """

    url = "%s/%s/%s/chatmessages" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME)

    payload = []

    if limit:
        payload.append("limit=%d" % limit)
    if cursor:
        payload.append("cursor=%s" % cursor)
    if ql:
        payload.append("ql=%s" % base64.urlsafe_b64encode(ql))

    if payload:
        url = ''.join((url, "?", "&".join(payload)))

    # 处理数据的另外方式
    # query = {"limit": limit, "cursor": cursor}
    # url = build_query_url(url, query)

    return get(url, auth)


def export_chat_media():
    u"""导出语音图片文件.

        官方暂未实现服务端.
    """

    pass


def offline_msg_count(auth, username):
    u"""获取未读消息数

        获取一个IM用户的未读消息数

        Path : /{org_name}/{app_name}/users/{owner_username}/offline_msg_count
        HTTP Method : GET
        URL Params : 无
        Request Headers : {“Authorization”:”Bearer ${token}”}
        Request Body ： 无
        Response Body ： “data” : {“v3y0kf9arx” : 0 } —- 用户名：v3y0kf9arx ，未读消息数：0条

    """

    url = "%s/%s/%s/users/%s/offline_msg_count" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME, username)
    return get(url, auth)
