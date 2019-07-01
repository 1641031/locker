from flask import Flask

app = Flask(__name__)

#-----------------------------------

# 读取配置文件
# config.py
from config import Config
app.config.from_object(Config)

#-----------------------------------

# 数据库flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
    # 数据库迁移包migrate
    # 子命令【flask db】集合
    # 使用案例
    # :$ flask db init 【来创建locker的迁移存储库】
    # :$ flask db migrate -m '备注名字'【把数据模型添加到 迁移脚本中, -m添加备注】
    # :$ flask db upgrade 【要更改应用到新版本数据库】
    # :$ flask db downgrade 【回滚上次的迁移】
    
from flask_migrate import Migrate
migrate = Migrate(app, db)

#-----------------------------------

# 登录验证，提供记住我 功能：允许用户在关闭浏览器窗口后再次访问应用时保持登录状态
from flask_login import LoginManager
login = LoginManager(app)
    #login为视图函数，表示未登录的用户查看受保护的页面时，重定向到登录界面
login.login_view = 'login'

#-----------------------------------

#bootstrap引入并实例化
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)


#--------------------------
#Flask-Moment 它将日期和时间转换成目前可以想象到的所有格式
from flask_moment import Moment
moment = Moment(app)

#-----------------------------------

# 引入
# app/routes.py路由

# 引入定义数据库结构模块
# app/models.py
from app import routes, models