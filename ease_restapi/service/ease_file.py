#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ring info client service sdk.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/23'

import os
import os.path
import requests

import six

from .. import config
from .base import http_result, build_file_rename, check_file_dir


def upload_media(auth, file_path):
    u"""上传语音图片.

        :param auth: 身份认证
        :param file_path: 文件路径

        所需要的 HTTP Header:
        * Authorization: 获取到的token
        * restrict-access: 是否限制访问权限,

        注意, 这个API并没有考虑这个属性的值, 而是有这个属性即可.
        最后, 需要使用http multipart/form-data 形式

        Path: /{org_name}/{app_name}/chatfiles
        HTTP Method: POST
        Request Headers: {“restrict-access”:true,”Authorization”:”Bearer ${token}”}
        URL Params: 无
        Request Body: 文件
        Response Body: 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    """

    file_rename = build_file_rename(os.path.basename(file_path))
    files = {'file': (file_rename, open(file_path, 'rb'), 'multipart/form-data', {'Expires': '0'})}

    required_header = {
        "restrict-access": True
    }

    six.print_('file_rename:', file_rename)
    url = "%s/%s/%s/chatfiles" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME)
    r = requests.post(url, files=files, headers=required_header, auth=auth)
    return http_result(r)


def write_file_data(res, file_name):
    u"""从远程下载文件写入数据到本地.

        :param res: 远程Response对象
        :param file_name: 本地文件名
    """

    down_file_dir = check_file_dir(os.path.join(os.getcwd(), 'download'))

    fp = None
    try:
        fp = open(os.path.join(down_file_dir, file_name), 'wb')
        fp.write(res.content)
        error = 0
    except IOError:
        error = 1
    finally:
        if fp:
            fp.close()

    return error


def download_media(auth, file_name, secret):
    u"""下载图片,语音文件.

        :param auth: 身份认证
        :param file_name: 文件名
        :param secret: 共享密匙

        这里需要注意的就是, 需要在http header中带上上面返回的 share-secret 和当前登陆用户的token才能够下载,
        同时注意header中执行的accept的值需要设置成 application/octet-stream

        curl -O
        -H "share-secret: DRGM8OZrEeO1vafuJSo2IjHBeKlIhDp0GCnFu54xOF3M6KLr"
        -H "Authorization: Bearer YWMtz1hFWOZpEeOPpcmw1FB0RwAAAUZnAv0D7y9-i4c9_c4rcx1qJDduwylRe7Y"
        -H "Accept: application/octet-stream"
        http://a1.easemob.com/easemob-demo/chatdemoui/chatfiles/0c0f5f3a-e66b-11e3-8863-f1c202c2b3ae
    """

    required_header = {
        "share-secret": secret,
        "Accept": "application/octet-stream"
    }

    url = "%s/%s/%s/chatfiles/%s" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME, file_name)
    res = requests.get(url, headers=required_header, auth=auth)

    return write_file_data(res, file_name)


def download_thumbnail(auth, file_name, secret):
    u"""下载缩略图.

        :param auth: 身份认证
        :param file_name: 文件名
        :param secret: 共享密匙

        环信支持在服务器短自动的创建图片的缩略图, 可以先下载缩略图, 当用户有需求的时候, 再下载大图
        这里和下载大图唯一不同的就是heaer中多了一个”thumbnail: true”,
        当服务器看到过来的请求的header中包括这个的时候, 就会返回缩略图, 否则返回原始大图

        curl -O
        -H "thumbnail: true"
        -H "share-secret: DRGM8OZrEeO1vafuJSo2IjHBeKlIhDp0GCnFu54xOF3M6KLr"
        -H "Authorization: Bearer YWMtz1hFWOZpEeOPpcmw1FB0RwAAAUZnAv0D7y9-i4c9_c4rcx1qJDduwylRe7Y"
        -H "Accept: application/octet-stream"
        http://a1.easemob.com/easemob-demo/chatdemoui/chatfiles/0c0f5f3a-e66b-11e3-8863-f1c202c2b3ae
    """

    required_header = {
        "thumbnail": True,
        "share-secret": secret,
        "Accept": "application/octet-stream"
    }

    url = "%s/%s/%s/chatfiles/%s" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME, file_name)
    res = requests.get(url, headers=required_header, auth=auth)

    return write_file_data(res, 'thumb_%s' % file_name)
