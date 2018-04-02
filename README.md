## TryScan - 自动化Sql注入检测工具
  * 通过普通浏览、操作网页，自动检测存在sql注入的漏洞
  * 浏览器端必须使用：[TryScanClient](https://github.com/ziiber/TryScan-Client)
  * 妈妈再也不用担心我找不到洞洞啦~  躺着也能挖洞

### 环境
* 开发框架：Flask
* 开发环境：python 3.x

### 安装使用
* 安装依赖 pip install -r requirement.txt
* 修改 config.py 配置文件
* 创建数据库 python manage.py create_all
* 启动调度器 python scheduler.py 
* 启动应用 python run.py


### 开发人员
* Try [ziiber@foxmail.com](http://ziiber.me)
* 时间：2016-07-22
