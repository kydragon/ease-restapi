## 环信服务器端实例代码

本实例使用了[request](http://docs.python-requests.org/en/latest/)类库来调用环信的REST API, 在运行本示例代码之前, 请先参考[这里](http://docs.python-requests.org/en/latest/user/install/)安装.

---

##本地开发说明
####本地代码在基于环信官方REST API的对接, 描述如下:
+ service包为对官方REST API的对接, 按功能模块依次组织代码, 文件名以"ease_"为前缀标识.
+ config.py为本地配置文件; common.py为本地公共类库; demo.py为service包的使用实例, 同时也是测试.
+ service包__init__.py提供REST API实现的对外调用.
+ gering包__init__.py提供环信与本地业务的对外调用.

#####本地代码与环信账户的链接, 有两种形式:
+ 本地表的形式, 以models.py, admin.py, chkinfos.py为个单元, 实现本地账户与环信账户的链接.
+ 官方建议形式, 以bridge.py为单元, 实现本地账户与环信账户的链接.
---

###遗留问题 
+ 基于版本：V2.0.9 2014-09-15
+ 后续官方REST API的一旦变动, service包的代码相应要微调.
+ urls.py, views.py, 待根据需要补全, 目前只保留用于web形式测试功能. 
