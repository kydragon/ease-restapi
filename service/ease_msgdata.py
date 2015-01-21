#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ring info client service sdk.
"""

__author__ = 'kylin'
__date__ = '2015/01/25'


class MessageData(object):
    """消息基础体
    """

    def __init__(self, target, target_type="users", username=None, **args):
        """
            :param target: 发送对象.
            :param target_type: 对象类型, users/chatgroups.
            :param username: 发送人, None会显示是admin.
            :param args: 扩展属性, 由app自己定义.
        """

        self._dict_data = {
            "target_type": target_type,
            "target": target,
            "msg": {
                "type": "txt"
            },
            "from": username,
            "ext": args
        }

    def __call__(self):
        raise NotImplementedError()


class MessageTxtData(MessageData):
    """文本消息体
    """

    def __init__(self, message,
                 target, target_type="users", username=None, **args):
        """
            :param message: 消息内容.
        """

        super(MessageTxtData, self).__init__(target, target_type=target_type, username=username, **args)
        self._dict_data["msg"]["msg"] = message

    def __call__(self):
        return self._dict_data


class MessageImgData(MessageData):
    """图片消息体
    """

    def __init__(self, url, filename, secret,
                 target, target_type="users", username=None, **args):
        """
            :param url: 成功上传文件返回的uuid
            :param filename: 指定一个文件名
            :param secret: 成功上传文件后返回的secret
        """

        super(MessageImgData, self).__init__(target, target_type=target_type, username=username, **args)

        self._dict_data["msg"]["type"] = "img"
        self._dict_data["msg"]["url"] = url
        self._dict_data["msg"]["filename"] = filename
        self._dict_data["msg"]["secret"] = secret

    def __call__(self):
        return self._dict_data


class MessageAudioData(MessageData):
    """语音消息体
    """

    def __init__(self, url, filename, length, secret,
                 target, target_type="users", username=None, **args):
        """
            :param url: 成功上传文件返回的uuid
            :param filename: 指定一个文件名
            :param length:  默认10
            :param secret:  成功上传文件后返回的secret
        """

        super(MessageAudioData, self).__init__(target, target_type=target_type, username=username, **args)

        self._dict_data["msg"]["type"] = "audio"
        self._dict_data["msg"]["url"] = url
        self._dict_data["msg"]["filename"] = filename
        self._dict_data["msg"]["length"] = length
        self._dict_data["msg"]["secret"] = secret

    def __call__(self):
        return self._dict_data


class MessageVideoData(MessageData):
    """视频消息体
    """

    def __init__(self, filename, thumb, length, secret, file_length, thumb_secret, url,
                 target, target_type="users", username=None, **args):
        """
            :param filename: 视频文件名称
            :param thumb: 成功上传视频缩略图返回的uuid
            :param length: 视频播放长度
            :param secret: 成功上传视频文件后返回的secret
            :param file_length: 视频文件大小
            :param thumb_secret: 成功上传视频缩略图后返回的secret
            :param url: 成功上传视频文件返回的uuid
        """

        super(MessageVideoData, self).__init__(target, target_type=target_type, username=username, **args)

        self._dict_data["msg"]["type"] = "video"
        self._dict_data["msg"]["filename"] = filename
        self._dict_data["msg"]["thumb"] = thumb
        self._dict_data["msg"]["length"] = length
        self._dict_data["msg"]["secret"] = secret
        self._dict_data["msg"]["file_length"] = file_length
        self._dict_data["msg"]["thumb_secret"] = thumb_secret
        self._dict_data["msg"]["url"] = url

    def __call__(self):
        return self._dict_data


class MessageTransmissionData(MessageData):
    """透传消息体
    """

    def __init__(self, action, target, target_type="users", username=None, **args):
        """
            :param action: action
        """

        super(MessageTransmissionData, self).__init__(target, target_type=target_type, username=username, **args)

        self._dict_data["msg"]["type"] = "cmd"
        self._dict_data["msg"]["action"] = action

    def __call__(self):
        return self._dict_data
