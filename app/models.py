# app/db.py
from app import db

# 时间戳
from datetime import datetime

# 哈希密码验证
from werkzeug.security import generate_password_hash, check_password_hash

# flask_login
from flask_login import UserMixin
from app import login
# 用户加载函数，Flask-Login将从会话中检索用户的ID，然后将该用户实例加载到内存中


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

    # 函数db.Column(字段, 可选参数)

    # 字段 --
    # db.Integer
    # db.String(num)
    # db.DateTime

    # 可选参数 --
    # primary_key= True/False 【是否为主键】
    # index = True/False 【是否可索引】
    # unique = True/False 【是否唯一】
    # default = datetime.utcnow   【将一个函数作为默认值传入后，SQLAlchemy会将该字段设置为调用该函数的值】

    # ---------------------------------------
    # 补充说明
    # 在“多”Post类中外键 连接设置方式
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #
    # ---------------------------------------

    # 一对多
    # 函数db.relationship(代表多的表名, 可选参数)   【建立外键】【通常在一这边定义】
    # 可选参数--
    # backref = 'author' 【参数定义了代表“多”的类的实例反向调用“一”名称】
    # lazy = 'dynamic' 【定义这种关系调用的数据库查询是如何执行的】

    # -----------------------------------------
    # 添加一个用户案例
    # u = User(username='susan', email='susan@example.com')
    # db.session.add(u)   【添加】
    # db.session.commit()   【应用，开始编译成SQL语句】
    # users = User.query.all() 【查询所有数据，返回一个集合】
    # u = User.query.get(1) 【获取指定序号ID的数据】

    # 以反向字母顺序获取所有用户
    # User.query.order_by(User.username.desc()).all()

    # UserMixin 通过mixin类实现四个属性或方法：
    # 1. is_authenticated: 一个用来表示用户是否通过登录认证的属性，用True和False表示。
    # 2. is_active: 如果用户账户是活跃的，那么这个属性是True，否则就是False
    # 3. is_anonymous: 常规用户的该属性是False，对特定的匿名用户是True
    # 4. get_id(): 返回用户的唯一id的方法，返回值类型是字符串


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    Lockers = db.relationship('Locker', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Locker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lockername = db.Column(db.String(32), index=True, unique=True)
    about_locker = db.Column(db.String(140))
    lockernumber = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.lockername)

class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goodsname = db.Column(db.String(32), index=True, unique=True)
    about_goods = db.Column(db.String(140))
    #储物箱
    locker_id = db.Column(db.Integer, db.ForeignKey('locker.id'),nullable=False)
    locker = db.relationship('Locker',backref=db.backref('goods', lazy=True))
    #分别标签
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('goods', lazy=True))

    def __repr__(self):
        return '<Post {}>'.format(self.goodsname)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Category {}>'.format(self.name)

class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    #保存对应物品的ID
    good_id = db.Column(db.Integer)
    #使用记录
    use_record = db.Column(db.String(140))
    #使用物品的时间
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Record {}>'.format(self.use_record)

