#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ring info client service sdk.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/23'

from .conf import HOST_SERVER, APP_ORG, APP_NAME
from .base import get, post, delete


def build_group_data(group_name, desc, owner, public, approval=True, members=None):
    u"""构建群组创建数据.

        :param group_name: 群组名称, 此属性为必须的
        :param desc: 群组描述, 此属性为必须的
        :param owner:"jma1", #群组的管理员, 此属性为必须的
        :param public:true, #是否是公开群, 此属性为必须的
        :param approval:true, #加入公开群是否需要批准, 没有这个属性的话默认是true, 此属性为可选的
        :param members:["jma2","jma3"] #群组成员,此属性为可选的
    """
    if not members:
        members = []

    dict_data = {
        "groupname": group_name,
        "desc": desc,
        "public": public,
        "approval": approval,
        "owner": owner,
        "members": members
    }

    return dict_data


def create_group(auth, group_data):
    u"""创建一个群组.

        :param auth: 身份认证
        :param group_data: 数据

        POST /{org_name}/{app_name}/chatgroups
        参数
        {
            "groupname":"testrestgrp12", //群组名称, 此属性为必须的
            "desc":"server create group", //群组描述, 此属性为必须的
            "public":true, //是否是公开群, 此属性为必须的
            "approval":true, //加入公开群是否需要批准, 没有这个属性的话默认是true, 此属性为可选的
            "owner":"jma1", //群组的管理员, 此属性为必须的
            "members":["jma2","jma3"] //群组成员,此属性为可选的
        }
    """

    url = HOST_SERVER + ("/%s/%s/chatgroups/" % (APP_ORG, APP_NAME))
    return post(url, payload=group_data, auth=auth)


def delete_group(auth, group_id):
    u"""删除群组.

        :param auth: 身份认证
        :param group_id: 群组ID, 注意: 非群组名称

        DELETE /{org_name}/{app_name}/chatgroups/{group_id}
    """

    url = HOST_SERVER + ("/%s/%s/chatgroups/%s" % (APP_ORG, APP_NAME, group_id))
    return delete(url, auth)


def details_group(auth, group_ids):
    u"""获取一个或者多个群组的详情.

            :param auth: 身份认证
            :param group_ids: 群组ID, 注意: 非群组名称

            GET /{org_name}/{app_name}/chatgroups/{group_id1},{group_id2}
        """

    url = HOST_SERVER + ("/%s/%s/chatgroups/%s" % (APP_ORG, APP_NAME, group_ids))
    return get(url, auth)


def pickup_group_users(auth, group_id):
    u"""获取群组中的所有成员.

        :param auth: 身份认证
        :param group_id: 群组ID, 注意: 非群组名称

        GET /{org_name}/{app_name}/chatgroups/{group_id}/users
    """

    url = HOST_SERVER + ("/%s/%s/chatgroups/%s/users/" % (APP_ORG, APP_NAME, group_id))
    return get(url, auth)


def pickup_groups(auth):
    u"""获取app中所有的群组ID.

        :param auth: 身份认证
        GET /{org_name}/{app_name}/chatgroups
    """

    url = HOST_SERVER + ("/%s/%s/chatgroups" % (APP_ORG, APP_NAME))
    return get(url, auth)


def user_join_group(auth, group_id, username):
    u"""在群组中添加一个人.

        :param auth: 身份认证
        :param group_id: 群组ID 注意: 非群组名称
        :param username: 用户

        POST /{org_name}/{app_name}/chatgroups/{group_id}/users/{user_primary_key}
    """

    url = HOST_SERVER + ("/%s/%s/chatgroups/%s/users/%s" % (APP_ORG, APP_NAME, group_id, username))
    return post(url, {}, auth)


def user_kick_group(auth, group_id, username):
    u"""在群组中减少一个人.

        :param auth: 身份认证
        :param group_id: 群组ID, 注意: 非群组名称
        :param username: 用户

        DELETE /{org_name}/{app_name}/chatgroups/{group_id}/users/{user_primary_key}
    """

    url = HOST_SERVER + ("/%s/%s/chatgroups/%s/users/%s" % (APP_ORG, APP_NAME, group_id, username))
    return delete(url, auth)