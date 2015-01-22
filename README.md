## 环信服务器端实例代码

本实例使用了[request](http://docs.python-requests.org/en/latest/)类库来调用环信的REST API, 在运行本示例代码之前, 请先参考[这里](http://docs.python-requests.org/en/latest/user/install/)安装.

---

##本地开发说明
####本地代码在基于环信官方REST API的对接, 描述如下:
+ service包为对官方REST API的对接, 按功能模块依次组织代码, 文件名以"ease_"为前缀标识.
+ config.py为本地配置文件; common.py为本地公共类库; demo.py为service包的使用实例, 同时也是测试.
+ service包__init__.py提供REST API实现的对外调用.
+ gering包__init__.py提供环信与本地业务的对外调用.
+ usage.py提供本地业务的调用注意点.

#####本地代码与环信账户的链接, 有两种形式:
+ 本地表的形式, 以models.py, admin.py, chkinfos.py为个单元, 实现本地账户与环信账户的链接.
+ 官方建议形式, 以bridge.py为单元, 实现本地账户与环信账户的链接.
---

###遗留问题 
+ 基于版本：2015-01-21
+ 后续官方REST API的一旦变动, service包的代码相应要微调.
+ urls.py, views.py, 待根据需要补全, 目前只保留用于web形式测试功能. 


###[环信ID规则](http://www.easemob.com/docs/rest/userapi/)

    当App和环信集成的时候, 需要把App系统内的已有用户和新注册的用户和环信集成, 为每个已有用户创建一个环信的账号(环信ID), 
    并且App有新用户注册的时候, 需要同步的在环信中注册.

    在注册环信账户的时候, 需要注意环信ID的规则:

        环信ID需要使用英文字母和（或）数字的组合
        环信ID不能使用中文
        环信ID不能使用email地址
        环信ID不能使用UUID
        环信ID中间不能有空格或者井号（#）等特殊字符
        允许的用户名正则 “[a-zA-Z0-9_\-./ ]*” (a~z大小写字母和数字和下划线和斜杠和横杠和英文点和反斜杠) 其他都不允许

    另: 本文档中可能会交错使用”环信ID”和”环信用户名”两个术语, 但是请注意, 这里两个的意思是一样的
