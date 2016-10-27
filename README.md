# 合作开发须知
1、为保证master分支的绝对稳定，除组长和副组长外不允许其他人直接合并修改到master分支，更不允许合并后推送到远程库；

2、大家需要在dev分支下面建立各自的分支，需要提交时合并到dev分支再提交；

3、开发环境统一用virtualenv搭建，具体需要安装模块参考requirement.txt，可切换到虚拟环境目录，使用命令pip install -r requirement.txt快速安装相应模块；Study目录下和右侧的Wiki会有相关的帮助文档。

4、代码说明：

4.1、目前已对各自负责模块进行了功能拆分，主要拆分了common、course和users模块，每个模块对应一个app，统一放在maizi目录下，大家按照各自负责的功能模块需求进行开发即可

4.2、templates下目录对应各自app模块所对应的页面，各自的页面放到各自对应的目录名下，基模板base.html和首页模板index.html已经拆分，可以直接使用，其他页面需从common/base.html继承（参照common/index.html）

4.3、Model统一都放到了common/models.py，Model由项目组长统一管理，common/admin.py后台的配置管理也有组长统一管理，其他组员不得擅自修改（修改前必须经由组长同意）

4.4、代码的规范统一采用PEP8编码规范，头部注释可参照已有代码文件中的注释方式

4.5、静态文件在模板中的调用统一都采用static标签的方式引入

4.6、url的配置统一都在各自的app下面的urls.py中完成

4.7、各自功能有重大更新时，可在后面添加更新日志


# 2015-11-3
项目初始化完成
