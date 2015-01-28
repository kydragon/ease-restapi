
Introduce:
----------
本实例使用了 *request*  <http://docs.python-requests.org/en/latest/>类库来调用环信的REST API,
在运行本示例代码之前, 请先参考 *这里* <http://docs.python-requests.org/en/latest/user/install/>安装.

Introductions
-------------
本地开发说明, 本地代码在基于环信官方REST API的对接, 分几部分描述如下.

ease_restapi:
=============
- service包为对官方REST API的对接, 按功能模块依次组织代码, 文件名以 *ease_* 为前缀标识.
- service包__init__.py提供REST API实现的对外调用.
- simplify包__init__.py提供环信与本地业务的对外调用, usage.py提供本地业务的调用注意点.
- config.py为包配置模板文件.
- demo包为本地账户与环信账户的对接的另一种形式.

project_demo:
=============
- 实用django生成项目.
- config.py为该项目ease-restapi配置文件.
- common.py为本地公共类库.
- demo.py为service包的使用实例, 同时也是测试.

Two Integration Mode:
=====================
本地代码与环信账户的链接, 有两种形式:
- 本地表的形式, 以demo中models.py, admin.py, chkinfos.py为个单元, 实现本地账户与环信账户的对接.
- 官方建议形式, 以simplify中bridge.py为单元, 实现本地账户与环信账户的对接.
- 环信ID规则: <http://www.easemob.com/docs/rest/userapi/>

Attention Note:
===============
- 基于版本：2015-01-21
- 后续官方REST API的一旦变动, service包的代码相应要微调.
- project_demo中urls.py, views.py, 请根据需要补全, 目前只保留用于web形式测试功能.

