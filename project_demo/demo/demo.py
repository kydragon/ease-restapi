#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ring info local code test, only test so on.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/25'

import os.path

import six

from ease_restapi.service import *
from ease_restapi.simplify.bridge import create_easemob_user
from .common import id_generator, get_json_path

from .config import (APP_KEY, CLIENT_ID, CLIENT_SECRET, OPEN_OR_CREDIT,
                     APP_ADMIN_USERNAME, APP_ADMIN_PASSWORD, ORG_ADMIN_PASSWORD, ORG_ADMIN_USERNAME)


APP_BASE_PATH = os.path.abspath(__file__)

if six.PY3:
    range_ = range
else:
    range_ = xrange


def test_org_admin_token():
    u"""org Admin token.
    """
    # org_admin的认证方式
    org_admin_auth = OrgAdminAccountAuth(ORG_ADMIN_USERNAME, ORG_ADMIN_PASSWORD)
    # 获取org管理员的token
    six.print_("Get org admin token: %s" % org_admin_auth.get_token())

    return org_admin_auth


def test_app_admin_token_passwd():
    u"""App Admin token.
    """
    # 获取app管理员的token
    app_admin_auth = AppAdminAccountAuth(APP_ADMIN_USERNAME, APP_ADMIN_PASSWORD)
    six.print_("Get app admin token:%s" % app_admin_auth.get_token())

    return app_admin_auth


def test_app_admin_token_client():
    u"""App Client token.
    """
    # 通过client id和secret来获取app管理员的token
    app_client_auth = AppClientAuth(CLIENT_ID, CLIENT_SECRET)
    six.print_("Get app admin token with client id/secret: %s" % app_client_auth.get_token())

    return app_client_auth


def test_register_user_open():
    u"""用户开放注册.
    """

    six.print_("now let's register some users....")

    app_users = []
    num_users = 1  # 10
    for _ in range_(num_users):
        username = id_generator()

        password = '123456'
        success, result = create_user_open(username, password)
        if success:
            six.print_("registered new user %s in appkey[%s]" % (username, APP_KEY))
            app_users.append(username)
        else:
            six.print_("failed to register new user %s in appkey[%s]" % (username, APP_KEY))

    return app_users


def test_register_user_credit():
    u"""用户授权注册.
    """

    app_auth = test_app_admin_token_passwd()
    # app_auth = test_app_admin_token_client()
    six.print_("now let's register some users....")

    app_users = []
    num_users = 1  # 10
    for _ in range_(num_users):
        username = id_generator()

        password = '123456'
        success, result = create_user_credit(app_auth, username, password)
        if success:
            six.print_("registered new user %s in appkey[%s]" % (username, APP_KEY))
            app_users.append(username)
        else:
            six.print_("failed to register new user %s in appkey[%s]" % (username, APP_KEY))

    return app_users


def test_del_user(username):
    u"""测试删除用户.

        :param username: 用户名
    """

    app_auth = test_app_admin_token_passwd()
    # app_auth = test_app_admin_token_client()
    success, result = delete_user(app_auth, username)
    if success:
        six.print_("user[%s] is deleted from appkey[%s]" % (username, APP_KEY))
        return 'ok'
    else:
        six.print_("failed to delete user[%s] from appkey[%s]" % (username, APP_KEY))
        return 'error'


def test_delete_user():
    u"""删除用户.
    """

    if OPEN_OR_CREDIT:
        app_users = test_register_user_credit()
    else:
        app_users = test_register_user_open()

    app_auth = test_app_admin_token_passwd()
    # app_auth = test_app_admin_token_client()

    six.print_("now let's delete users just created, this time we're using app_client_auth")

    org_count = len(app_users)
    cur_count = 0

    for username in app_users:
        success, result = delete_user(app_auth, username)
        if success:
            cur_count += 1
            six.print_("user[%s] is deleted from appkey[%s]" % (username, APP_KEY))
        else:
            six.print_("failed to delete user[%s] from appkey[%s]" % (username, APP_KEY))

    return {'org_count': org_count, 'cur_count': cur_count}


def test_remain_user(step=None):
    u"""测试账户信息修改.

        :param step: [1,2] 测试步骤, 两个步骤中的一个.
    """

    app_auth = test_app_admin_token_passwd()
    # app_auth = test_app_admin_token_client()
    six.print_("now let's update user info.")

    # 要测试模块函数:
    username = 'kylinfish'
    success, result = 'None', 'None'

    if step == 1:
        success, result = pickup_user(app_auth, username=username)
    elif step == 2:
        old_password = '123456789'
        new_password = '123456abc'
        success, result = passwd_user(app_auth, username=username, new_password=new_password, old_password=old_password)

    return success, result


def test_send_file():
    u"""发送文件.
    """

    app_auth = test_app_admin_token_passwd()
    # app_auth = test_app_admin_token_client()
    six.print_("now let's send an image")

    # 测试官方Demo失败:
    # success, result = send_file(app_client_auth, get_json_path(APP_BASE_PATH, 'zjg.jpg'))

    # 测试成功:
    success, result = upload_media(app_auth, get_json_path(APP_BASE_PATH, 'zjg.jpg'))

    six.print_(result)

    return success, result


def test_down_file():
    u"""测试下载文件.
    """

    app_auth = test_app_admin_token_passwd()
    # app_auth = test_app_admin_token_client()
    six.print_("now let's download an image")

    # entity = {
    # "uuid": "030dec90-4489-11e4-a778-fb4c6c765344",
    # "share-secret": "Aw3smkSJEeSPXNE5zuNMkHfiBVQIUFnkTQQcrqEZuHD38PdQ"
    # }

    entity = {
        "uuid": "fbd7d450-4491-11e4-8025-2d9f8838aa1b",
        "share-secret": "-9fUWkSREeSXRNcQQpDV_-Y0w-7VRm0wvLhX4VrzYysRIQvz"
    }

    # result = download_media(app_auth, file_name=entity["uuid"], secret=entity["share-secret"])
    result = download_thumbnail(app_auth, file_name=entity["uuid"], secret=entity["share-secret"])

    return result


def test_friend(step=None):
    u"""测试ease_friend模块.

        :param step: [1,2,3] 测试步骤, 三个步骤中的一个.
    """

    app_auth = test_app_admin_token_passwd()
    # app_auth = test_app_admin_token_client()
    six.print_("now let's friend module testing")

    # 要测试模块函数:
    success, result = 'None', 'None'

    owner_username = 'kylinfish'
    friend_username = 'huixian'

    if step == 1:
        success, result = create_friend(app_auth, owner_username, friend_username)
    elif step == 2:
        success, result = delete_friend(app_auth, owner_username, friend_username)
    elif step == 3:
        success, result = detail_friend(app_auth, owner_username)

    return success, result


def test_group(step=None):
    u"""测试ease_group模块.

        :param step: [1,2,3,4,5,6,7] 测试步骤, 七个步骤中的一个.
    """

    app_auth = test_app_admin_token_passwd()
    # app_auth = test_app_admin_token_client()
    six.print_("now let's group module testing")

    # 要测试模块函数:
    success, result = 'None', 'None'

    if step == 1:
        owner_username = 'kylinfish'

        group_name, desc, public = 'mojiGroup', 'moji group test', True
        # group_name, desc, public = 'mojiGroupX', 'moji group test', True

        group_data = build_group_data(group_name, desc, owner_username, public)
        success, result = create_group(app_auth, group_data)

    elif step == 2:
        success, result = pickup_groups(app_auth)

        # {"groupname": "mojiGroup", "groupid": "1411873543593435"}
        # {"groupname": "mojiGroupX", "groupid": "141187358674801"}

    elif step == 3:
        group_id = "141187358674801"
        success, result = delete_group(app_auth, group_id)

    else:
        group_id = "1411873543593435"

        if step == 4:
            success, result = details_group(app_auth, group_id)
        elif step == 5:
            success, result = pickup_group_users(app_auth, group_id)

        else:
            join_username = 'huixian'

            if step == 6:
                success, result = user_join_group(app_auth, group_id, join_username)
            elif step == 7:
                success, result = user_kick_group(app_auth, group_id, join_username)

    return success, result


def test_message(step=None):
    u"""测试ease_message模块.

        :param step: [1,2] 测试步骤, 两个步骤中的一个.
    """

    app_auth = test_app_admin_token_passwd()
    # app_auth = test_app_admin_token_client()
    six.print_("now let's message module testing")

    # 要测试模块函数:
    success, result = 'None', 'None'
    target = ['huixian', ]

    if step == 1:
        username = ['kylinfish', None]
        message = "hello world, my name is kylinfish."

        dict_data = build_message_data(message, target, username=username[0])
        success, result = send_txt_message(app_auth, dict_data)

    elif step == 2:
        success, result = look_user_status(app_auth, target[0])

    return success, result


def test_records():
    u"""测试ease_records模块.
    """

    app_auth = test_app_admin_token_passwd()
    # app_auth = test_app_admin_token_client()
    six.print_("now let's records module testing")

    # 要测试模块函数:
    # success, result = 'None', 'None'
    success, result = export_chat_message(app_auth)

    six.print_(result)

    return success, result


def test_batch(step=None):
    u"""测试ease_batch模块.

        :param step: [1,2,3] 测试步骤, 三个步骤中的一个.
    """

    app_auth = test_app_admin_token_passwd()
    # app_auth = test_app_admin_token_client()
    six.print_("now let's batch module testing")

    # 要测试模块函数:
    success, result = 'None', 'None'

    if step == 1:
        play_load = [
            {'username': 'juguang', 'password': '123456'},
            {'username': 'wangshu', 'password': '123456'},
            {'username': 'kaiwen', 'password': '123456'}
        ]

        success, result = create_users(app_auth, play_load)
    elif step == 2:
        success, result = pickup_users(app_auth)
    elif step == 3:
        ql = "order by created desc"
        success, result = delete_users(app_auth, ql=ql, limit=2)

    return success, result


def test_select(step=None):
    u"""测试ease_select模块.

        :param step: 步骤
    """

    app_auth = test_app_admin_token_passwd()
    # app_auth = test_app_admin_token_client()
    six.print_("now let's select module testing")

    # 要测试模块函数:
    # success, result = 'None', 'None'
    if step:
        ql = "select * where username='kylin'"
    else:
        ql = None

    success, result = select_users(app_auth, ql=ql)
    return success, result


def test_main():
    u"""测试代码
    """

    # 测试成功:
    # test_org_admin_token()
    # test_app_admin_token_passwd()
    # test_app_admin_token_client()
    # result = 'ok'

    # 开放注册:
    # result = test_register_user_open()

    # result = test_del_user("37NE67")
    # result = test_delete_user()

    # 授权注册:
    # result = test_register_user_credit()
    # result = test_delete_user(True)

    # result = test_send_file()
    # result = test_down_file()

    # result = 'to-do...'
    # result = test_friend()
    # result = test_group()
    # result = test_message()
    # result = test_records()
    # result = test_batch()
    # result = test_select(True)
    # result = test_remain_user(2)

    result = create_easemob_user('78569@qq.com', '123456')

    return result


if __name__ == '__main__':
    u"""单元测试
    """

    test_main()

    # six.print_(CLIENT_ID, '|', CLIENT_SECRET)

    # pass
