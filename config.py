import os

# 获取应用顶级目录path
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # 加密秘钥，通知Flask读取并使用安全秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Flask-SQLAlchemy插件从SQLALCHEMY_DATABASE_URI配置变量中获取应用的数据库的位置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # 数据库配置发送改变后是否发送信号给应用
    SQLALCHEMY_TRACK_MODIFICATIONS = False
