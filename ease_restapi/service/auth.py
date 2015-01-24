#!/usr/bin/python
# -*- coding: utf-8 -*-

"""ring info auth code.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/20'

from time import time
from requests.auth import AuthBase

import six

from .. import config
from .base import post


class MeToken(object):
    u"""表示一个登陆获取到的token对象.
    """

    def __init__(self, token, expires_in):
        self.token = token
        self.expires_in = expires_in + int(time())

        six.print_('|', expires_in, '|')
        six.print_('token:', self.token)
        six.print_('expires:', self.expires_in)

    def is_not_valid(self):
        u"""这个token是否还合法, 或者说, 是否已经失效了, 这里我们只需要
        检查当前的时间, 是否已经比或者这个token的时间过去了expires_in秒.

        即current_time_in_seconds < (expires_in + token_acquired_time)
        """

        return time() > self.expires_in

    def __str__(self):
        return self.token

    def __unicode__(self):
        return self.token


class ServiceAuth(AuthBase):
    u"""环信登陆认证的基类.
    """

    def __init__(self):
        self.token = None

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer %s' % self.get_token()
        return r

    def get_token(self):
        u"""在这里我们先检查是否已经获取过token, 并且这个token有没有过期.
        """

        if self.token is None or self.token.is_not_valid():
            # refresh the token
            self.token = self.acquire_token()

        return str(self.token)

    def acquire_token(self):
        u"""真正的获取token的方法, 返回值是一个我们定义的Token对象.
            这个留给子类去实现.
        """
        pass


class AppClientAuth(ServiceAuth):
    u"""使用app的client_id和client_secret来获取app管理员token.
    """

    def __init__(self, client_id, client_secret):
        super(AppClientAuth, self).__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.url = "%s/%s/%s/token" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME)
        self.token = None

    def acquire_token(self):
        u"""使用client_id/client_secret来获取token.

            具体的REST API为:
            POST /{org}/{app}/token
            {'grant_type':'client_credentials', 'client_id':'xxxx', 'client_secret':'xxxxx'}
        """

        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        success, result = post(self.url, payload)
        if success:
            return MeToken(result['access_token'], result['expires_in'])
        else:
            # throws exception
            pass

        return self.token


class AppAdminAccountAuth(ServiceAuth):
    u"""使用app的管理员账号和密码来获取token.
    """

    def __init__(self, username, password):
        super(AppAdminAccountAuth, self).__init__()
        self.username = username
        self.password = password
        self.url = "%s/%s/%s/token" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME)
        self.token = None

    def acquire_token(self):
        u"""使用username/password来获取token.

            具体的REST API为:
            POST /{org}/{app}/token {'grant_type':'password', 'username':'xxxx', 'password':'xxxxx'}
            这里和上面使用client_id不同的是, grant_type的类型是password, 然后还需要提供username和password
        """

        payload = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password
        }

        success, result = post(self.url, payload)
        if success:
            if config.EXPIRES_IN:
                self.token = MeToken(result['access_token'], config.EXPIRES_IN)
            else:
                self.token = MeToken(result['access_token'], result['expires_in'])
        else:
            # throws exception
            pass

        return self.token


class OrgAdminAccountAuth(ServiceAuth):
    u"""使用org的管理员账号和密码来获取token.

        注意:
        1.获取的是整个org的管理员账号, 所以没有app_key的概念.
          这里使用的URL是 https://a1.easemob.com/management/token.

        2.和上面不同, 因为没有app_key的概念, 所以URL也不相同.
          而上面app级别的token都是 https://a1.easemob.com/{org}/{app}/token.
    """

    def __init__(self, username, password):
        super(OrgAdminAccountAuth, self).__init__()
        self.username = username
        self.password = password
        self.url = "%s/management/token" % config.HOST_SERVER
        self.token = None

    def acquire_token(self):
        u"""使用username/password来获取token.

            具体的REST API为:
            POST /management/token {'grant_type':'password', 'username':'xxxx', 'password':'xxxxx'}
        """

        payload = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password
        }

        success, result = post(self.url, payload)
        if success:
            if config.EXPIRES_IN:
                self.token = MeToken(result['access_token'], config.EXPIRES_IN)
            else:
                self.token = MeToken(result['access_token'], result['expires_in'])
        else:
            # throws exception
            pass

        return self.token


def get_app_auth(mode=0):
    if mode == 0:
        return
    elif mode == 1:
        return AppClientAuth(config.APP_ADMIN_USERNAME, config.APP_ADMIN_PASSWORD)
    elif mode == 2:
        OrgAdminAccountAuth(config.APP_ADMIN_USERNAME, config.APP_ADMIN_PASSWORD)


APP_AUTH = get_app_auth
