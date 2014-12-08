#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ring info remote api conf data required.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/20'

try:
    from django.conf import settings

    DEBUG = getattr(settings, "DEBUG", True)
except (ImportError, Exception):
    DEBUG = True

from ..config import APP_KEY, APP_ORG, APP_NAME, CLIENT_ID, CLIENT_SECRET
from ..config import org_admin_username, org_admin_password, app_admin_username, app_admin_password


# ORG Admin info:
ORG_ADMIN_USERNAME = org_admin_username
ORG_ADMIN_PASSWORD = org_admin_password

# APP Admin info：
APP_ADMIN_USERNAME = app_admin_username
APP_ADMIN_PASSWORD = app_admin_password

# APP Config info：
APP_KEY = APP_KEY
APP_ORG = APP_ORG
APP_NAME = APP_NAME

CLIENT_ID = CLIENT_ID
CLIENT_SECRET = CLIENT_SECRET

# APP download storage:
DIR_DOWNLOAD_FILES = ''

JSON_HEADER = {'content-type': 'application/json'}
HOST_SERVER = 'https://a1.easemob.com'
