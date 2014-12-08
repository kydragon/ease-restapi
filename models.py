#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ring info data model.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/22'

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import check_password, make_password


class RingInfoManager(models.Manager):
    u"""环信客户信息
    """

    def get_ring_uid(self, user):
        u"""环信客户信息项

            :param user: 用户
        """

        ring_info = None
        try:
            ring_info = self.get(user=user)
        except RingInfo.DoesNotExist:
            pass
        except RingInfo.MultipleObjectsReturned:
            pass
        return ring_info

    def get_ring_cid(self, username):
        u"""环信客户信息项

            :param username: 账户
        """

        ring_info = None
        try:
            ring_info = self.get(username=username)
        except RingInfo.DoesNotExist:
            pass
        except RingInfo.MultipleObjectsReturned:
            pass
        return ring_info

    def ring_uid_exists(self, user):
        u"""判断环信客户信息项是否存在

            :param user: 用户
        """

        ring_info = self.get_ring_uid(user=user)
        if ring_info:
            return True
        else:
            return False

    def ring_cid_exists(self, username):
        u"""判断环信客户信息项是否存在

            :param username: 账户
        """

        ring_info = self.get_ring_cid(username=username)
        if ring_info:
            return True
        else:
            return False

    def create_ring_info(self, user, username, password):
        u"""创建环信客户信息项

            :param user: 用户
            :param username: 账户
            :param password: 密码
        """

        ring_info = self.model(user=user, username=username, password=password)
        ring_info.save(using=self._db)

        return ring_info


class RingInfo(models.Model):
    u"""环信客户信息
    """

    id = models.AutoField(primary_key=True, verbose_name=_('auto ID'))
    user = models.ForeignKey(User, related_name='ring_user', verbose_name=_('user'))

    username = models.CharField(_('username'), max_length=30, unique=True)
    password = models.CharField(_('password'), max_length=15)
    # password = models.CharField(_('password'), max_length=128) # 加密

    status = models.BooleanField(_('activate status'), default=True)
    add_date = models.DateTimeField(_('insert datetime'), auto_now_add=True)

    objects = RingInfoManager()

    class Meta:
        db_table = 'third_ring_info'
        verbose_name = _('ring info')
        verbose_name_plural = _('ring info list')
        unique_together = (("user", "username"),)

    def __unicode__(self):
        return "%s %s" % self.natural_key()

    def natural_key(self):
        return (
            self.user, self.username
        )

    def update_info(self, **dicts):
        u"""设置并更新指定字段的值

            :param dicts
        """

        for (key, value) in dicts.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def set_password(self, raw_password):
        u""""如果使用加密密码

            :param raw_password: 密码
        """

        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        u"""
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.

            :param raw_password: 密码
        """

        def setter(password):
            self.set_password(password)
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)
