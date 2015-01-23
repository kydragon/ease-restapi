#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ring info client service sdk.
"""

__author__ = 'kylinfish@126.com'
__date__ = '2014/09/20'

from .. import config
from .base import get, post


def build_message_data(message, target, target_type="users", username=None, **args):
    u"""构建消息发送数据.

        :param message: 消息内容.
        :param target: 发送对象.
        :param target_type: 对象类型, users/chatgroups.
        :param username: 发送人, None会显示是admin.
        :param args: 扩展属性, 由app自己定义.

        args:
            data = {'key1':1,'key2':2}
            build_message_data(...,**data)
            build_message_data(...,key1=1,key2=2)
    """

    if not isinstance(target, list):
        return 8888

    if target_type not in ["users", "chatgroups"]:
        return 8888

    dict_data = {
        "target_type": target_type,
        "target": target,
        "msg": {
            "type": "txt",
            "msg": message
        },
        "from": username,
        "ext": args
    }

    return dict_data


def look_user_status(auth, username):
    u"""查看用户在线状态.

        :param auth: 身份认证
        :param username: 用户名

        查看一个用户的在线状态
        Path : /{org_name}/{app_name}/users/{user_primary_key}/status
        HTTP Method : GET
        URL Params ： 无
        Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
        Request Body ： 无
        Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    """

    url = "%s/%s/%s/users/%s/status" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME, username)
    return get(url, auth)


def send_message(auth, dict_data):
    u"""发送消息.

        :param auth: 身份认证
        :param dict_data: 数据

        Path : /{org_name}/{app_name}/messages
        Request Method : POST
        URL Params ： 无
        Request Headers : {“Content-Type”:”application/json”,”Authorization”:”Bearer ${token}”}
        Response Body ： 详情参见示例返回值, 返回的json数据中会包含除上述属性之外的一些其他信息，均可以忽略。
    """

    url = "%s/%s/%s/messages" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME)
    return post(url, payload=dict_data, auth=auth)


def send_txt_message(auth, dict_data):
    u"""发送文本消息.

        :param auth: 身份认证
        :param dict_data: 数据

        给一个或者多个用户, 或者一个或者多个群组发送消息, 并且通过可选的_from_字段让接收方看到发送
        方是不同的人,同时, 支持扩展字段, 通过_ext_属性, app可以发送自己专属的消息结构.

        Request Body ：
        {
            "target_type" : "users", or chatgroups
            "target" : ["u1", "u2", "u3"], //注意这里需要用数组, 即使只有一个用户, 也要用数组 ['u1']
            "msg" : {
                "type" : "txt",
                "msg" : "hello from rest" 消息内容, 参考[聊天记录]
                    (http://developer.easemob.com/docs/emchat/rest/chatmessage.html)里的bodies内容.
                },
            "from" : "jma2", 表示这个消息是谁发出来的, 可没有这个属性, 那就显示是admin, 如果有的话, 则显示是这个用户发出的
            "ext" : { 扩展属性, 由app自己定义
                "attr1" : "v1",
                "attr2" : "v2"
            }
        }
    """

    return send_message(auth, dict_data)


def send_img_message(auth, dict_data):
    u"""发送图片消息

        :param auth: 身份认证
        :param dict_data: 数据

        给一个或者多个用户, 或者一个或者多个群组发送消息, 并且通过可选的 from 字段让接收方看到发送方是不同的人,同时, 支持扩展字段,
        通过 ext 属性, app可以发送自己专属的消息结构.

        为保证接口调用安全性，该接口有限流控制。同一个IP地址每秒钟最多可以调用30次。
        如果该限流控制不满足需求，请联系商务经理开放更高的权限。

        Request Body ：
        {
            "target_type" : "users",   //users 给用户发消息, chatgroups 给群发消息
            "target" : ["u1", "u2", "u3"],// 注意这里需要用数组,数组长度建议不大于20, 即使只有一个用户,
                                          // 也要用数组 ['u1'], 给用户发送时数组元素是用户名,给群组发送时
                                          // 数组元素是groupid
            "msg" : {  //消息内容
                "type" : "img",   // 消息类型
                "url": "https://a1.easemob.com/easemob-demo/chatdemoui/chatfiles/55f12940-64af-11e4-8a5b-ff2336f03252",
                 //成功上传文件返回的uuid
                "filename": "24849.jpg", // 指定一个文件名
                "secret": "VfEpSmSvEeS7yU8dwa9rAQc-DIL2HhmpujTNfSTsrDt6eNb_" // 成功上传文件后返回的secret
             },
            "from" : "jma2",
            //表示这个消息是谁发出来的, 可以没有这个属性, 那么就会显示是admin, 如果有的话, 则会显示是这个用户发出的
            "ext" : { //扩展属性, 由app自己定义.可以没有这个字段，但是如果有，值不能是“ext:null“这种形式，否则出错
                "attr1" : "v1",
                "attr2" : "v2"
            }
        }
    """

    return send_message(auth, dict_data)


def send_audio_message(auth, dict_data):
    u"""发送语音消息

        :param auth: 身份认证
        :param dict_data: 数据

        发送语音文件，需要先上传语音文件，然后再发送此消息。（url中的uuid和secret可以从上传后的response获取）
        为保证接口调用安全性，该接口有限流控制。同一个IP地址每秒钟最多可以调用30次。如果该限流控制不满足需求，请联系商务经理开放更高的权限。

        Request Body ：
        {
            "target_type" : "users",  //users 给用户发消息, chatgroups 给群发消息
            "target" : ["testd", "testb", "testc"],// 注意这里需要用数组,数组长度建议不大于20, 即使只有一个
                                                   // 用户或者群组, 也要用数组形式 ['u1'], 给用户发送
                                                   // 此数组元素是用户名,给群组发送时数组元素是groupid
            "msg" : {   //消息内容
                "type": "audio",  // 消息类型
                "url": "https://a1.easemob.com/easemob-demo/chatdemoui/chatfiles/1dfc7f50-55c6-11e4-8a07-7d75b8fb3d42",
                 //成功上传文件返回的uuid
                "filename": "messages.amr", // 指定一个文件名
                "length": 10,
                "secret": "Hfx_WlXGEeSdDW-SuX2EaZcXDC7ZEig3OgKZye9IzKOwoCjM" // 成功上传文件后返回的secret
            },
            "from" : "testa" ,
            //表示这个消息是谁发出来的, 可以没有这个属性, 那么就会显示是admin, 如果有的话, 则会显示是这个用户发出的
            "ext" : { //扩展属性, 由app自己定义.可以没有这个字段，但是如果有，值不能是“ext:null“这种形式，否则出错
                    "attr1" : "v1",
                    "attr2" : "v2"
                }
        }
    """

    url = "%s/%s/%s/messages" % (config.HOST_SERVER, config.APP_ORG, config.APP_NAME)
    return post(url, payload=dict_data, auth=auth)


def send_video_message(auth, dict_data):
    u"""发送视频消息

        :param auth: 身份认证
        :param dict_data: 数据

        发送视频消息，需要先上传视频文件和视频缩略图文件，然后再发送此消息。（url中的uuid和secret可以从上传后的response获取）
        为保证接口调用安全性，该接口有限流控制。同一个IP地址每秒钟最多可以调用30次。
        如果该限流控制不满足需求，请联系商务经理开放更高的权限。


        Request Body ：
        {
            "target_type": "users", //users 给用户发消息, chatgroups 给群发消息
            "target": [
                "ceshib"// 注意这里需要用数组,数组长度建议不大于20, 即使只有一个，// 用户或者群组, 也要用数组形式 ['u1'], 给用户发送
            ], // 此数组元素是用户名,给群组发送时数组元素是groupid
            "from": "ceshia",
            "msg": { //消息内容
                "type": "video",// 消息类型
                "filename": "1418105136313.mp4",// 视频文件名称
                "thumb": "http://a1.easemob.com/easemob-demo/chatdemoui/chatfiles/67279b20-7f69-11e4-8eee-21d3334b3a97",
                //成功上传视频缩略图返回的uuid
                "length": 10,//视频播放长度
                "secret": "VfEpSmSvEeS7yU8dwa9rAQc-DIL2HhmpujTNfSTsrDt6eNb_",// 成功上传视频文件后返回的secret
                "file_length": 58103,//视频文件大小
                "thumb_secret": "ZyebKn9pEeSSfY03ROk7ND24zUf74s7HpPN1oMV-1JxN2O2I",// 成功上传视频缩略图后返回的secret
                "url": "http://a1.easemob.com/easemob-demo/chatdemoui/chatfiles/671dfe30-7f69-11e4-ba67-8fef0d502f46"
                //成功上传视频文件返回的uuid
            }
        }
    """

    return send_message(auth, dict_data)


def send_transmission_message(auth, dict_data):
    u"""发送透传消息

        :param auth: 身份认证
        :param dict_data: 数据

        透传消息：
            不会在客户端提示（铃声，震动，通知栏等），但可以在客户端监听到的消息推送，具体功能可以根据自身自定义
            为保证接口调用安全性，该接口有限流控制。同一个IP地址每秒钟最多可以调用30次。
            如果该限流控制不满足需求，请联系商务经理开放更高的权限。

        Request Body ：
        {
            "target_type":"users",     // users 给用户发消息,  chatgroups 给群发消息
            "target":["testb","testc"], // 注意这里需要用数组,数组长度建议不大于20, 即使只有
                                        // 一个用户u1或者群组, 也要用数组形式 ['u1'], 给用户发
                                        // 送时数组元素是用户名,给群组发送时数组元素是groupid
            "msg":{  //消息内容
                "type":"cmd",  // 消息类型
                "action":"action1"
            },
            "from":"testa",  //表示这个消息是谁发出来的, 可以没有这个属性, 那么就会显示是admin, 如果有的话, 则会显示是这个用户发出的
            "ext":{   //扩展属性, 由app自己定义.可以没有这个字段，但是如果有，值不能是“ext:null“这种形式，否则出错
                "attr1":"v1",
                "attr2":"v2"
            }
        }
    """

    return send_message(auth, dict_data)








