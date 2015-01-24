#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

u"""
集成后:
    注册(附带)
    修改密码(附带)
    删除账户(附带)

集成前:
    集成前的账户信息, 要适应集成后的机制来保证数据的完整性.
    建议本地账户信息(比如: UserProfile), 增加环信账户状态字段. 比如: ring_info, 初始值为: False, 完成环信注册后为: True.

可能修改:
    根据本地业务修改的, 可能的修改如下.

    check_user_id:      账户生成方式.
    chalk_remote_user:  密码生成方式.
    join_easemob_local: 环信账户状态字段, 本地账户昵称字段.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/28'
__doc__ = 'local and ring-info code integration.'

import hmac
import hashlib
import six

from ease_restapi import config
from ease_restapi.service import (AppAdminAccountAuth, create_user_open, create_user_credit,
                                  passwd_user, pickup_user, modify_nickname)


class HashFunction(object):
    @classmethod
    def mac_new(cls, password):
        """hmac."""

        new_password = hmac.new(config.APP_KEY, password, hashlib.md5).hexdigest()
        return new_password

    @classmethod
    def hash_mode(cls, password, hash_class):
        """add another mode."""

        return hash_class(password).hexdigest()


class BothFunction(object):
    @classmethod
    def python(cls, password):
        """java develop fell not easy.
        """

        # import this code.

        password = ''.join((config.APP_KEY, password))

        d = {}
        for c in (65, 97):
            for i in range(26):
                d[chr(i + c)] = chr((i + 13) % 26 + c)
        new_password = "".join([d.get(c, c) for c in password])
        return new_password


def check_user_id(local_username):
    u"""环信ID规则检测, 生成环信用户名

    :param local_username: 本地用户名

    环信ID需要使用英文字母和（或）数字的组合
        环信ID不能使用中文
        环信ID不能使用email地址
        环信ID不能使用UUID
        环信ID中间不能有空格或者井号（#）等特殊字符
    """

    # 因为邮箱登陆机制, 所以做简单替换生成环信账户处理.
    remote_username = local_username.replace('@', '_')

    # 除上规则, 还可以使用以下两种方式生成账户:
    # HashFunction: 考虑到在好友列表, 会话列表项, 如果要在客户端显示本地昵称, 需要反向推导, 有此需求不要使用以下方式.
    # remote_username = HashFunction.hash_mode(local_username, hashlib.md5)

    # BothFunction: 可以满足反向推导.
    # see pycrypto packae, you can more.
    # remote_username = BothFunction.python(local_username)

    return remote_username


def check_remote_user(auth, remote_username):
    u"""检测环信某个账户名是否已经存在.

        此函数的功能主要是出于, 本地系统在集成环信前, 早期即有账户的过渡可能需要.

        :param auth: 身份认证
        :param remote_username: 环信用户名
    """

    remote_user_exist = False
    success, result = pickup_user(auth, username=remote_username)

    if success:
        if 'entities' in result and len(result["entities"]) > 0:
            remote_user_exist = True

    return remote_user_exist


def chalk_remote_user(local_username, local_password):
    u"""根据本地用户信息, 生成环信账户的映射.

        :param local_username: 用户名, 第三方用户体系中的primary_key, 需要在app_key的范围内唯一.

        :param local_password: 用户密码.
            为保证第三方用户体系中的账号密码不必要的泄露给环信, 建议对第三方用户体系的账号密码做一次hash算法.
            然后在手机端登录环信时, 客户端同样适用hash后的密码登录.
    """

    local_username = check_user_id(local_username)
    local_password = HashFunction.hash_mode(local_password, hashlib.md5)

    return local_username, local_password


def create_easemob_user(local_username, local_password):
    u"""从本地账户创建环信账户.

        使用: 将该函数的调用使用在本地系统的账户注册里, 根据该函数的结果做记录处理.

        :param local_username:本地账户名
        :param local_password: 本地账户密码
    """

    if not config.SWITCH_JOIN_LOCAL:
        return False

    remote_username, remote_password = chalk_remote_user(local_username, local_password)

    if config.OPEN_OR_CREDIT:
        app_auth = AppAdminAccountAuth(config.APP_ADMIN_USERNAME, config.APP_ADMIN_PASSWORD)
        success, result = create_user_credit(app_auth, remote_username, remote_password)
    else:
        success, result = create_user_open(remote_username, remote_password)
    if success:
        flag = True
    else:
        flag = False

    return flag


def passwd_easemob_user(local_username, local_password):
    u"""本地账户密码修改, 影响环信账户的密码修改.

        :param local_username:本地账户名
        :param local_password: 本地账户密码
    """

    if not config.SWITCH_JOIN_LOCAL:
        return False

    remote_username, remote_password = chalk_remote_user(local_username, local_password)
    app_auth = AppAdminAccountAuth(config.APP_ADMIN_USERNAME, config.APP_ADMIN_PASSWORD)
    success, result = passwd_user(app_auth, remote_username, remote_password)
    if success:
        flag = True
    else:
        flag = False

    return flag


def change_easemob_nickname(local_username, local_nickname):
    u"""本地账户密码修改, 影响环信账户的密码修改.

        :param local_username:本地账户名
        :param local_nickname: 本地账户昵称
    """

    if not config.SWITCH_JOIN_LOCAL:
        return False

    remote_username = check_user_id(local_username)
    app_auth = AppAdminAccountAuth(config.APP_ADMIN_USERNAME, config.APP_ADMIN_PASSWORD)
    success, result = modify_nickname(app_auth, remote_username, local_nickname)
    if success:
        flag = True
    else:
        flag = False

    return flag


def join_easemob_local(user_profile, username, password, saved=False):
    u"""环信系统集成到本地系统.

        检测集成与否->集成->如果集成成功, 则保存.

        :param user_profile:本地账户信息表model类实例.

        :param username: 本地账户
        :param password:本地密码
        :param saved: 是否保存,如果外层调用该代码之后有保存,这里就默认False, 反之True.
    """

    result = False
    if not user_profile.ring_join:
        result = create_easemob_user(local_username=username, local_password=password)
    if result:
        user_profile.ring_join = 1

        # Fixed:
        # http://www.easemob.com/docs/android/setnickname/

        # 此方法主要为了在苹果推送时能够推送昵称(nickname)而不是userid.
        # 一般可以在登陆成功后从自己服务器获取到个人信息, 然后拿到nick更新到环信服务器.
        # 并且, 在个人信息中如果更改个人的昵称, 也要把环信服务器更新下nickname 防止显示差异.

        # 如果自己用户体系有昵称, 则更新到环信.
        # user_profile.name 为本地用户昵称字段, 变通需注意.
        if user_profile.name:
            try:
                change_easemob_nickname(username, user_profile.name)
            except Exception as e:
                # 对此过程不做一定成功处理.
                six.print_(e)

        if saved:
            user_profile.save()

    return user_profile
