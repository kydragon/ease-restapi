#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ring info client service sdk.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/20'

from .auth import AppClientAuth, AppAdminAccountAuth, OrgAdminAccountAuth, APP_AUTH

from .ease_select import select_users
from .ease_batch import create_users, delete_users, pickup_users, add_group_users
from .ease_friend import create_friend, delete_friend, detail_friend

from .ease_user import create_user_open, create_user_credit, delete_user, passwd_user, pickup_user, modify_nickname

from .ease_file import upload_media, download_media, download_thumbnail

from .ease_group import user_join_group, user_kick_group, modify_group, pickup_group_users, pickup_user_group
from .ease_group import build_group_data, create_group, delete_group, details_group, pickup_groups

from .ease_msgdata import MessageTxtData, MessageImgData, MessageAudioData, MessageVideoData, MessageTransmissionData
from .ease_message import (build_message_data, look_user_status, send_txt_message, send_img_message,
                           send_audio_message, send_video_message, send_transmission_message)

from .ease_records import export_chat_message, export_chat_media, offline_msg_count
from .ease_black import add_user_blacklist, del_user_blacklist, pickup_user_blacklist
