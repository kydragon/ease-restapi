#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/20'

from .common import duct_json
from .demo import test_main


def test(request):
    u"""预留测试.
    """

    if request.method != 'POST':
        return duct_json({'error': 9999})


def debug(request):
    u"""暂时, 用于代码调试.
    """

    result_data = test_main()

    return duct_json({'error': 0, 'data': result_data})
