#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/20'

from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
                       url(r'^test/$', test, name='test'),
                       url(r'^debug/$', debug, name='debug'), )
