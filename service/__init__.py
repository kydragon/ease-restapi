#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/20'
__doc__ = 'ring info client service sdk.'

from .auth import AppClientAuth, AppAdminAccountAuth, OrgAdminAccountAuth

from .ease_select import select_users
from .ease_batch import create_users, delete_users, pickup_users
from .ease_friend import create_friend, delete_friend, detail_friend

from .ease_user import create_user_open, create_user_credit, delete_user, passwd_user, pickup_user

from .ease_file import upload_media, download_media, download_thumbnail

from .ease_group import user_join_group, user_kick_group, pickup_group_users
from .ease_group import build_group_data, create_group, delete_group, details_group, pickup_groups

from .ease_message import build_message_data, send_message, look_user_status
from .ease_records import export_chat_message
