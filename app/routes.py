# 全局域包
import logging

from datetime import datetime

from app import db
from flask_login import logout_user
from werkzeug.urls import url_parse
from flask import request
from app.forms import LoginForm
from flask import render_template
from app import app

# flash 提示用户的动作是否成功， redirect 重定向 , url_for 与路由函数绑定链接
from flask import flash, redirect, url_for


# 加载flask_login包，
# current_user!!!
from flask_login import current_user, login_user

#app/models.py ----User类
from app.models import User,Locker,Category


# -------------------------------------------------------------

# 主页
from flask_login import login_required
@app.route('/')
@app.route('/index')
# 当匿名用户(未登录的用户)查看首页时，重定向到登录界面
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home Page', posts=posts)


# 用户登录----------------------------------------
# 读取和处理 next 查询字符串参数【重定向相关辅助包】
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 确认用户是否通过登录认证的属性[是否登录]
    if current_user.is_authenticated:
        # 如果没登录，是匿名用户，就重定向到主页index，index 会判断是否为匿名用户，是的话就再重定向login界面
        return redirect(url_for('index'))
    form = LoginForm()
    # 当点击表单的submit时触发
    if form.validate_on_submit():
        # filter_by 结果是一个只包含具有匹配用户名的对象的查询结果集
        user = User.query.filter_by(username=form.username.data).first()
        # 如果user或没，或者没有通过嘻哈密码验证
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            # 重定向登录页面
            return redirect(url_for('login'))
        # 登录成功
        # 通过login_user函数可以获取next查询字符串参数的值
        # 该函数会将用户登录状态注册为已登录
        login_user(user, remember=form.remember_me.data)
        # Flask提供一个request变量，其中包含客户端随请求发送的所有信息。
        # 特别是request.args属性，可用友好的字典格式暴露查询字符串的内容
        next_page = request.args.get('next')
        # 为了确定URL是相对的还是绝对的，我使用Werkzeug的url_parse()函数解析，然后检查netloc属性是否被设置。
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


# 用户登出-------------------------------
@app.route('/logout')
def logout():
    # 该函数将current_user变为登出状态
    logout_user()
    return redirect(url_for('index'))


# 用户注册视图------------------------------
# app/db.py
from app.forms import RegistrationForm
# app/forms.py ---RegistrationForm类
@app.route('/register', methods=['GET', 'POST'])
def register():
    # 确定用户是否登录
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    #获取表单中的注册表类，建立实例
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# 记录最后访问时间[before_request视图函数之前执行的函数]
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# 储物柜总视图------------
@app.route('/lockerview', methods=['GET', 'POST'])
@login_required
def lockerview():
    #普通用户权限
    # nowuser = User.query.filter_by(username=current_user.username).first
    #最高权限
    # if current_user.username == "user":
    if Locker.query.all():
        lockers = Locker.query.all()
    else:
        lockers = ""
    # else:
    #     print(nowuser.Lockers)
    #     if nowuser.Lockers:
    #         lockers = nowuser.Lockers
    #     else:
    #         lockers = ""
    return render_template('lockerview.html', lockers=lockers)


# 储物空间创建
from app.forms import CreateLocker
@app.route('/createlocker', methods=['GET', 'POST'])
@login_required
def createlocker():
    form = CreateLocker()
    # 如果触发form实例对象中的submit的该事件。
    if form.validate_on_submit():
        locker = Locker(lockername=form.lockername.data,
                        lockernumber=form.lockernumber.data, about_locker=form.about_locker.data,author=current_user)
        db.session.add(locker)
        db.session.commit()
        flash("Your locker is have been created!")
        return redirect(url_for('lockerview'))
    return render_template('createlocker.html', title='CreateLocker', form=form)


# 编辑储物空间
from app.forms import EditLocker
@app.route('/edit_locker/<lockerid>', methods=['GET','POST'])
@login_required
def edit_locker(lockerid):
    form = EditLocker()
    locker = Locker.query.get(lockerid)
    if form.validate_on_submit():
        locker.lockername = form.lockername.data
        locker.lockernumber = form.lockernumber.data
        locker.about_locker = form.about_locker.data
        db.session.add(locker)
        db.session.commit()
        flash("your edit is over")
        return redirect(url_for('lockerview'))
    elif request.method == 'GET':
        form.lockername.data = locker.lockername
        form.lockernumber.data = locker.lockernumber
        form.about_locker.data = locker.about_locker
    return render_template('edit_locker.html', title="Edit locker",form=form)

# 删除储物空间
from app.forms import DeleteLocker
@app.route('/delete_locker/<lockerid>', methods=['GET','POST'])
@login_required
def delete_locker(lockerid):
    form = DeleteLocker()

    if form.validate_on_submit():
        locker = Locker.query.get(lockerid)
        if locker.lockername == form.lockername.data:
            db.session.delete(locker)
            db.session.commit()
            flash("space is deleted!")
            return redirect(url_for('lockerview'))
        else:
            form.lockername = ""
            flash("name is wrong!you have to check it!")
    return render_template('delete_locker.html', title="delete locker",form=form)



#创建标签
from app.forms import CreateCategory
@app.route('/create_category', methods=['GET','POST'])
@login_required
def create_category():
    form = CreateCategory()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash("Category is successded")
        return redirect(url_for('goods'))
    return render_template('create_category.html', title='Create_Category', form=form)



# #物品页面 --总展示页面-----------
@app.route('/goods', methods=['GET', 'POST'])
# 当匿名用户(未登录的用户)查看首页时，无法重定向到登录界面
@login_required
def goods():
    if Category.query.all():
        categorys = Category.query.all()
    else:
        categorys = ""
    return render_template('goods.html',categorys=categorys)