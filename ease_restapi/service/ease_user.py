#!/usr/bin/python
# -*- coding: utf-8 -*-

u"""ring info user system local code.

    注册IM用户[单个]
    在url指定的org和app中创建一个新的用户, 分两种模式：开放注册 和 授权注册.
    "开放注册"模式: 注册环信账号时不用携带管理员身份认证信息.
    "授权注册"模式: 注册环信账号必须携带管理员身份认证信息.
    推荐使用"授权注册", 这样可以防止某些已经获取了注册url和知晓注册流程的人恶意向服务器大量注册垃圾用户.
    注意：以下api中提到的${token}是用户的具体token值, 企业管理员和app管理员的token均可.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/20'

from .. import config
from .base import get, put, post, delete


def create_user_open(username, password):
    u"""开放注册.

        :param username: 用户名
        :param password: 密码

        Path : /{org_name}/{app_name}/users
        HTTP Method : POST
        URL Params ： 无
        Request Headers : {“Content-Type”:”application/json”}
        Request Body ： {“username”:”${用户名}”,”password”:”${密码}”}
        Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。

        curl -X POST
        -i "https://a1.easemob.com/easemob-demo/chatdemo/users"
        -d '{"username":"jliu","password":"123456"}'

    """

    payload = {"username": username, "password": password}
    url = "%s/%s/%s/users" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME)
    return post(url, payload=payload)


def create_user_credit(auth, username, password):
    u"""授权注册.

        :param auth: 身份认证
        :param username: 用户名
        :param password: 密码

        Path : /{org_name}/{app_name}/users
        HTTP Method : POST
        URL Params ： 无
        Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
        Request Body ： {“username”:”${用户名}”,”password”:”${密码}”}
        Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。

        curl -X POST
        -H "Authorization: Bearer YWMt39RfMMOqEeKYE_GW7tu81AAAAT71lGijyjG4VUIC2AwZGzUjVbPp_4qRD5k"
        -i  "https://a1.easemob.com/easemob-demo/chatdemo/users"
        -d '{"username":"jliu","password":"123456"}'

    """

    payload = {"username": username, "password": password}
    url = "%s/%s/%s/users" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME)
    return post(url, payload=payload, auth=auth)


def delete_user(auth, username):
    u"""删除用户.

        :param auth: 身份认证
        :param username: 用户名

        DELETE /{org}/{app}/users/{username}
    """

    url = "%s/%s/%s/users/%s" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME, username)
    return delete(url, auth)


def passwd_user(auth, username, new_password, old_password=None):
    u""""置IM用户密码.

        :param auth: 身份认证
        :param username: 用户名
        :param new_password: 新密码
        :param old_password: 老密码

        Path : /{org_name}/{app_name}/users/{user_primary_key}/password
        HTTP Method : PUT
        URL Params : 无
        Request Headers : {“Authorization”:”Bearer ${token}”}
        Request Body ： {“newpassword” : “${新密码指定的字符串}”}
        Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    """

    payload = {"newpassword": new_password}
    if old_password:
        payload["old_password"] = old_password

    url = "%s/%s/%s/users/%s/password" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME, username)
    return put(url, payload, auth)


def pickup_user(auth, username):
    u"""获取IM用户[主键查询].

        :param auth: 身份认证
        :param username: 用户名

        对users来说，有两个primary key: username 和 uuid,通过他们都可以获取到一个用户

        Path : /{org_name}/{app_name}/users/{user_primary_key}
        HTTP Method : GET
        URL Params ：无
        Request Headers : {“Authorization”:”Bearer ${token}”}
        Request Body ： 无
        Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。

        1) username as user_primary_key
        2) uuid as user_primary_key

    """

    url = "%s/%s/%s/users/%s" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME, username)
    return get(url, auth)


def modify_nickname(auth, username, nickname):
    """修改用户昵称.

        Path : /{org_name}/{app_name}/users/{username}
        HTTP Method : PUT
        URL Params : 无
        Request Headers : {“Authorization”:”Bearer ${token}”}
        Request Body ： {“nickname” : “${昵称值}”}
        Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    """

    payload = {"nickname": nickname}
    url = "%s/%s/%s/users/%s" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME, username)
    return put(url, payload, auth)
