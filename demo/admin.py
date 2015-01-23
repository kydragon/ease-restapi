#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/20'

from django.contrib import admin
from .models import RingInfo


class RingInfoAdmin(admin.ModelAdmin):
    u"""自定义ModelAdmin.
    """

    list_display = ('id', 'user', 'username', 'password', 'status', 'add_date',)

    ordering = ('-id',)
    list_filter = ('status', 'add_date',)
    search_fields = ('user__username', 'username',)


admin.site.register(RingInfo)
# admin.site.register(RingInfo, RingInfoAdmin)