# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""ring info model check.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/22'

from .models import RingInfo


def check_ring_info(user, username):
    u"""检测新建注册信息.

        :param user: 用户
        :param username: 账户
        :return -1:用户已注册环信账户; -2:注册账户名已存在.
    """

    if RingInfo.ring_uid_exists(user=user):
        return -1

    if RingInfo.ring_cid_exists(username=username):
        return -2


def enable_ring_info(ring_info, action=True):
    u"""环信账户,禁用或激活.

        :param ring_info: 信息项
        :param action: 激活/禁用
    """

    if ring_info and isinstance(ring_info, RingInfo):
        ring_info.status = action
        ring_info.save()
        return 0

    return -1


def passwd_ring_info(ring_info, password, encrypt=False):
    u"""环信账户,更换密码.

        :param ring_info: 信息项
        :param password: 密码
        :param encrypt: 是否加密
    """

    if ring_info and isinstance(ring_info, RingInfo):
        if encrypt:
            ring_info.set_password(password)
        else:
            ring_info.password = password

        ring_info.save()
        return 0

    return -1


def delete_ring_info(user):
    u"""删除环信账户信息.

        :param user: 用户
    """

    RingInfo.objects.filter(user=user).delete()
    return 0
