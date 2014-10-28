#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
集成后:
    注册(附带)
    修改密码(附带)
    删除账户(附带)

集成前:
    集成前的账户信息, 要适应集成后的机制来保证数据的完整性.
    建议本地账户信息(比如: UserProfile), 增加环信账户状态字段. 比如: ring_info, 初始值为: False, 完成环信注册后为: True.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/28'
__doc__ = 'local and ring-info code integration.'

import hmac
from hashlib import sha1

from .config import APP_KEY, OPEN_OR_CREDIT, SWITCH_JOIN_LOCAL, app_admin_username, app_admin_password
from .service import AppAdminAccountAuth, create_user_open, create_user_credit, passwd_user, pickup_user


def check_remote_user(auth, local_username):
    u"""检测环信某个账户名是否已经存在.

        此函数的功能主要是出于, 本地系统在集成环信前, 早期即有账户的过渡可能需要.
    """

    remote_user_exist = False
    success, result = pickup_user(auth, username=local_username)

    if success:
        if 'entities' in result and len(result["entities"]) > 0:
            remote_user_exist = True

    return remote_user_exist


def chalk_remote_user(local_username, local_password):
    u"""根据本地用户信息, 生成环信账户的映射.

        username: username.
            是第三方用户体系中的primary_key, 需要在app_key的范围内唯一.

        password: 密码.
            为保证第三方用户体系中的账号密码不必要的泄露给环信, 建议对第三方用户体系的账号密码做一次hash算法.
            然后在手机端登录环信时, 客户端同样适用hash后的密码登录.
    """

    remote_password = hmac.new(APP_KEY, local_password, sha1).digest()
    return local_username, remote_password


def create_easemob_user(local_username, local_password):
    u"""从本地账户创建环信账户

        使用: 将该函数的调用使用在本地系统的账户注册里, 根据该函数的结果做记录处理.

        :local_username:本地账户名
        :local_password: 本地账户密码
    """

    if not SWITCH_JOIN_LOCAL:
        return False

    remote_username, remote_password = chalk_remote_user(local_username, local_password)

    if OPEN_OR_CREDIT:
        app_auth = AppAdminAccountAuth(app_admin_username, app_admin_password)
        success, result = create_user_credit(app_auth, remote_username, remote_password)
    else:
        success, result = create_user_open(remote_username, remote_password)
    if success:
        flag = True
    else:
        flag = False

    return flag


def passwd_easemob_user(local_username, local_password):
    u"""本地账户密码修改, 影响环信账户的密码修改

        :local_username:本地账户名
        :local_password: 本地账户密码
    """

    if not SWITCH_JOIN_LOCAL:
        return False

    app_auth = AppAdminAccountAuth(app_admin_username, app_admin_password)
    remote_username, remote_password = chalk_remote_user(local_username, local_password)

    success, result = passwd_user(app_auth, remote_username, remote_password)
    if success:
        flag = True
    else:
        flag = False

    return flag


def join_easemob_local(user_profile, username, password, saved=False):
    u"""环信系统集成到本地系统.

        检测集成与否->集成->如果集成成功, 则保存.

        :user_profile:本地账户信息表model类实例.

        :username: 本地账户
        :password:本地密码
        :saved: 是否保存,如果外层调用该代码之后有保存,这里就默认False, 反之True.
    """

    result = False
    if not user_profile.ring_join:
        result = create_easemob_user(local_username=username, local_password=password)
    if result:
        user_profile.ring_join = 1

        if saved:
            user_profile.save()

    return user_profile
