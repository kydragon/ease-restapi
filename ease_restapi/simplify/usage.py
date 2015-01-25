# !/usr/bin/env python
# -*- coding: utf-8 -*-

import six

from ease_restapi import join_easemob_local, passwd_easemob_user, change_easemob_nickname


def login(request):
    u"""登录
    """

    profile = None
    username = None
    password = None

    # 登陆成功后调用执行如下代码：
    # 接入环信, 新注册用户自动接入
    join_easemob_local(profile, username, password, True)

    return


def user_joining(request):
    u"""用户注册
    """

    profile = None
    username = None
    password = None

    # 注册成功后调用执行如下代码：
    # 接入环信, 新注册用户自动接入
    join_easemob_local(profile, username, password, True)


def user_passwd_reset(request):
    u"""重置密码
    """

    user = None
    profile = None
    username = None
    password = None

    # 修改本地密码属性后执行如下代码：
    # 接入环信, 用户密码自动修改
    is_flag = True
    if profile.ring_join:
        is_flag = passwd_easemob_user(username, password)

    try:
        if is_flag:
            user.save()
        else:
            six.print_(u"环信密码更新失败.")
    except Exception as e:
        is_flag = False
        six.print_((e, u"本地数据密码保存失败."))

    if not is_flag:
        return {'error': 1010}  # u'密码重置失败'

    return


def user_profile(request):
    u"""修改会员信息
    """

    profile = None
    username = None
    nickname = None
    password = None

    # 修改昵称, 修改密码分别执行如下代码：
    # 接入环信, 用户昵称自动修改
    if profile.ring_join:
        change_easemob_nickname(username, nickname)

    # 接入环信, 用户密码自动修改
    passwd_easemob_user(username, password)

    return


def user_nickname(request):
    u"""从环信端用户名获取本地用户昵称.

        环信好友列表, 会话列表, username值传入该接口, 以本地昵称形式显示客户端.

        本地业务如有调整, 启用并修改下面注释代码, 增修字段.
    """

    if request.method != 'POST':
        return {'error': 9999}

    # 传入环信用户账户列表
    user_name_list = None if 'usernames' not in request.POST else request.POST['usernames']
    if not user_name_list:  # or user_name_list.count('@') > 0:  # 强制必须为环信规则
        return {'error': 8888}

    # 分解用户账户列表
    void_list = []
    is_error = False
    user_nick_list = []
    for user_name in user_name_list.split(','):
        # 找到最后个'_', 替换为'@'
        try:
            # 如本地业务的用户名与环信username映射规则有变, 修改以下两行.
            char_ind = user_name.rindex('_')
            user_name = '@'.join((user_name[:char_ind], user_name[char_ind + 1:]))

            user_nick_list.append(user_name)
        except (ValueError, Exception):
            # is_error = True
            # break
            void_list.append({'name': user_name})  # , ['field1': '','field2': '']})

            if is_error:
                return {'error': 8888}

    user_info_list = None  # [model].objects.filter([field]__in=user_nick_list).values(['field1', 'field2'])
    user_info_list = list(user_info_list)
    user_info_list.extend(void_list)

    return {'error': 0, 'array': user_info_list}