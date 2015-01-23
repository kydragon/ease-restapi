#!/usr/bin/python
# -*- coding: utf-8 -*-

"""ring info friend system local code.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/22'

from .. import config
from .base import get, post, delete


def create_friend(auth, owner_username, friend_username):
    u"""添加好友, 给一个用户添加好友, 好友必须是和自己在一个app下的IM用户.

        :param auth: 身份认证
        :param owner_username: 是要添加好友的用户名
        :param friend_username: 是被添加的用户名

        Path : /{org_name}/{app_name}/users/{owner_username}/contacts/users/{friend_username}
        HTTP Method : POST
        URL Params : 无
        Request Headers : {“Authorization”:”Bearer ${token}”}
        Request Body ： 无
        Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    """

    url = "%s/%s/%s/users/%s/contacts/users/%s" % (
        config.HOST_SERVER, config.APP_ORG, config.APP_NAME, owner_username, friend_username)
    return post(url, {}, auth)


def delete_friend(auth, owner_username, friend_username):
    u"""解除好友关系.

        :param auth: 身份认证
        :param owner_username: 是要添加好友的用户名
        :param friend_username: 是被删除的用户名

        Path : /{org_name}/{app_name}/users/{owner_username}/contacts/users/{friend_username}
        HTTP Method : DELETE
        URL Params : 无
        Request Headers : {“Authorization”:”Bearer ${token}”}
        Request Body ： 无
        Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    """

    url = "%s/%s/%s/users/%s/contacts/users/%s" % (
        config.HOST_SERVER, config.APP_ORG, config.APP_NAME, owner_username, friend_username)
    return delete(url, auth)


def detail_friend(auth, owner_username):
    u"""查看好友, 查看某个IM用户的好友信息.

        :param auth: 身份认证
        :param owner_username: 要查看好友用户名

        Path : /{org_name}/{app_name}/users/{owner_username}/contacts/users
        HTTP Method : GET
        URL Params : 无
        Request Headers : {“Authorization”:”Bearer ${token}”}
        Request Body ： 无
        Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    """

    url = "%s/%s/%s/users/%s/contacts/users/" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME, owner_username)
    return get(url, auth)
