#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""ring info black list local code.
"""

__author__ = 'kylin'
__date__ = '2015/01/20'

from .. import config
from .base import get, post, delete


def add_user_blacklist(auth, username, usernames):
    """往IM用户的黑名单中加人, 往一个IM用户的黑名单中加人.

        :param auth: 身份认证
        :param username: 用户名
        :param usernames: 要加入到黑名单中的用户名

        Path : /{org_name}/{app_name}/users/{owner_username}/blocks/users
        HTTP Method : POST
        URL Params : 无
        Request Headers : {“Authorization”:”Bearer ${token}”}
        Request Body ： {“usernames”:[“5cxhactgdj”, “mh2kbjyop1”]} —- 需要加入到黑名单中的用户名以数组方式提交，usernames为关键字不变，
        Response Body ： “data” : [ “5cxhactgdj”, “mh2kbjyop1” ] — 已经加到黑名单中的用户名：5cxhactgdj, mh2kbjyop1
    """

    payload = {"usernames": usernames}
    url = "%s/%s/%s/users/%s/blocks/users" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME, username)
    return post(url, payload=payload, auth=auth)


def del_user_blacklist(auth, username, blocked_username):
    """从IM用户的黑名单中减人, 从一个IM用户的黑名单中减人.

        :param auth: 身份认证
        :param username: 用户名
        :param blocked_username: 要减账户名

        Path : /{org_name}/{app_name}/users/{owner_username}/blocks/users/{blocked_username}
        HTTP Method : DELETE
        URL Params : 无
        Request Headers : {“Authorization”:”Bearer ${token}”}
        Request Body ：无
        Response Body ： entities 中包含了刚刚从黑名单中移除的IM用户的详细信息
    """

    url = "%s/%s/%s/users/%s/blocks/users/%s" % (
        config.HOST_SERVER, config.APP_ORG, config.APP_NAME, username, blocked_username)
    return delete(url, auth)


def pickup_user_blacklist(auth, username):
    """"获取IM用户的黑名单, 获取一个IM用户的黑名单.

        :param auth: 身份认证
        :param username: 用户名

        Path : /{org_name}/{app_name}/users/{owner_username}/blocks/users
        HTTP Method : GET
        URL Params : 无
        Request Headers : {“Authorization”:”Bearer ${token}”}
        Request Body ： 无
        Response Body ： “data” : [ “stliu2” ] — 黑名单中的用户的用户名：stliu2
    """

    url = "%s/%s/%s/users/%s/blocks/users" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME, username)
    return get(url, auth)

