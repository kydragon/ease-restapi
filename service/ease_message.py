#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ring info client service sdk.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/20'

from .conf import HOST_SERVER, APP_ORG, APP_NAME
from .base import get, post


def build_message_data(message, target, target_type="users", username=None, **args):
    u"""构建消息发送数据.

        :param message: 消息内容.
        :param target: 发送对象.
        :param target_type: 对象类型, users/chatgroups.
        :param username: 发送人, None会显示是admin.
        :param args: 扩展属性, 由app自己定义.

        args:
            data = {'key1':1,'key2':2}
            build_message_data(...,**data)
            build_message_data(...,key1=1,key2=2)
    """

    if not isinstance(target, list):
        return 8888

    if target_type not in ["users", "chatgroups"]:
        return 8888

    dict_data = {
        "target_type": target_type,
        "target": target,
        "msg": {
            "type": "txt",
            "msg": message
        },
        "from": username,
        "ext": args
    }

    return dict_data


def send_message(auth, dict_data):
    u"""发送消息.

        :param auth: 身份认证
        :param dict_data: 数据

        给一个或者多个用户, 或者一个或者多个群组发送消息, 并且通过可选的_from_字段让接收方看到发送
        方是不同的人,同时, 支持扩展字段, 通过_ext_属性, app可以发送自己专属的消息结构.

        Path : /{org_name}/{app_name}/messages
        Request Method : POST
        URL Params ： 无
        Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
        Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
        Request Body ：
        {
            "target_type" : "users", or chatgroups
            "target" : ["u1", "u2", "u3"], //注意这里需要用数组, 即使只有一个用户, 也要用数组 ['u1']
            "msg" : {
                "type" : "txt",
                "msg" : "hello from rest" 消息内容, 参考[聊天记录]
                    (http://developer.easemob.com/docs/emchat/rest/chatmessage.html)里的bodies内容.
                },
            "from" : "jma2", 表示这个消息是谁发出来的, 可没有这个属性, 那就显示是admin, 如果有的话, 则显示是这个用户发出的
            "ext" : { 扩展属性, 由app自己定义
                "attr1" : "v1",
                "attr2" : "v2"
            }
        }
    """

    url = HOST_SERVER + ("/%s/%s/messages" % (APP_ORG, APP_NAME))
    return post(url, payload=dict_data, auth=auth)


def look_user_status(auth, username):
    u"""查看用户在线状态.

        :param auth: 身份认证
        :param username: 用户名

        查看一个用户的在线状态
        Path : /{org_name}/{app_name}/users/{user_primary_key}/status
        HTTP Method : GET
        URL Params ： 无
        Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
        Request Body ： 无
        Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    """

    url = HOST_SERVER + ("/%s/%s/users/%s/status" % (APP_ORG, APP_NAME, username))
    return get(url, auth)
