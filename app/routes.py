# -*- coding: UTF-8 -*-
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
from app.models import User,Locker,Category,Goods,Record


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
    return render_template('/locker/lockerview.html', lockers=lockers)


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
    return render_template('/locker/createlocker.html', title='CreateLocker', form=form)


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
    return render_template('/locker/edit_locker.html', title="Edit locker",form=form)

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
    return render_template('/locker/delete_locker.html', title="delete locker",form=form)



#创建分类标签
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
    return render_template('/category/create_category.html', title='Create_Category', form=form)

#编辑分类标签
from app.forms import EditCategory
@app.route('/edit_category/<categoryid>', methods=['GET','POST'])
@login_required
def edit_category(categoryid):
    form = EditCategory()
    category = Category.query.get(categoryid)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.add(category)
        db.session.commit()
        flash("your category is deleted")
        return redirect(url_for('goods'))
    elif request.method == 'GET':
        form.name.data = category.name
    return render_template('/category/edit_category.html', title='Edit_Category', form=form)


#删除分类标签
from app.forms import DeleteCategory
@app.route('/delete_category/<categoryid>', methods=['GET','POST'])
@login_required
def delete_category(categoryid):
    form = DeleteCategory()
    if form.validate_on_submit():
        category = Category.query.get(categoryid)
        if category.name == form.name.data:
            db.session.delete(category)
            db.session.commit()
            flash("Category is deleted!")
            return redirect(url_for('goods'))
        else:
            form.name = ""
            flash("name is wrong!you have to check it!")
    return render_template('/category/delete_category.html', title="delete category",form=form)


#登录物品信息
from app.forms import Login_Goods
@app.route('/login_goods/', methods=['GET','POST'])
@login_required
def login_goods():

    form = Login_Goods()
    # form = Login_Goods(request.method, obj=locker)
    # form.locker_id.choices = [(g.lockername) for g in locker]
    # 如果触发form实例对象中的submit的该事件。
    if form.validate_on_submit():
        goods = Goods(goodsname=form.goodsname.data,locker=form.locker.data,category=form.category.data,about_goods=form.about_goods.data)
        db.session.add(goods)
        db.session.commit()
        # print(form.locker.data)
        flash("Your goods is have been created!")
        return redirect(url_for('goods'))
    return render_template('/goods/login_goods.html', title='Login_Good', form=form)

#编辑物品信息
from app.forms import Edit_Goods
@app.route('/edit_goods/<goodsid>', methods=['GET','POST'])
@login_required
def edit_goods(goodsid):
    form = Edit_Goods()
    goods = Goods.query.get(goodsid)
    if form.validate_on_submit():
        goods.goodsname = form.goodsname.data
        goods.about_goods = form.about_goods.data
        goods.locker = form.locker.data
        goods.category = form.category.data
        db.session.add(goods)
        db.session.commit()
        flash("your goods is Edited")
        return redirect(url_for('goods'))
    elif request.method == 'GET':
        form.goodsname.data = goods.goodsname
        form.about_goods.data =  goods.about_goods
        form.locker.data = goods.locker
        form.category.data =  goods.category
    return render_template('/goods/edit_goods.html', title='Edit_Category', form=form)

#删除物品
#删除分类标签
from app.forms import Delete_Goods
@app.route('/delete_goods/<goodsid>', methods=['GET','POST'])
@login_required
def delete_goods(goodsid):
    form = Delete_Goods()
    if form.validate_on_submit():
        goods= Goods.query.get(goodsid)
        if goods.goodsname == form.goodsname.data:
            db.session.delete(goods)
            db.session.commit()
            flash("Goods is deleted!")
            return redirect(url_for('goods'))
        else:
            form.name = ""
            flash("name is wrong!you have to check it!")
    return render_template('/goods/delete_goods.html', title="delete goods",form=form)

##物品页面 --总展示页面-----------

@app.route('/goods', methods=['GET', 'POST'])
# 当匿名用户(未登录的用户)查看首页时，无法重定向到登录界面
@login_required
def goods():

    if Category.query.all():
        categorys = Category.query.all()
    else:
        categorys = ""
    if Goods.query.all():
        goods = Goods.query.all()
        # record = Goods_Record() 
    else:
        goods = ""
    return render_template('/goods/goods.html',categorys=categorys,goods=goods)





from app.forms import Goods_Record
#**
# from steppermotor.StepperTest import CreateLocker
#**
@app.route('/record/<goodsid>', methods=['GET', 'POST'])
@login_required
def record(goodsid):
    #**
    # stepper = CreateLocker()
    #**
    form = Goods_Record()
    goods = Goods.query.get(goodsid)
    user = User.query.get(current_user.id)
    if form.validate_on_submit():
        record = Record(good_id=goodsid,use_record=form.use_record.data)
        user = User.query.get(current_user.id)
        db.session.add(record)
        # **
        # stepnum=int(stepper.move(user.now_num, goods.locker.lockernumber, user.locker_distance, user.maxlockernum))
        # print(stepnum)
        # stepper.begin(stepnum)
        # user.now_num = goods.locker.lockernumber
        # db.session.add(user)
        # **
        db.session.commit()
        flash("record is over!")
        return redirect(url_for('goods'))
    return render_template('/goods/record.html',form=form,goods=goods)

@app.route('/query_record/<goodsid>', methods=['GET', 'POST'])
@login_required
def query_record(goodsid):
    querys = Record.query.filter_by(good_id=goodsid).all()
    return render_template('/goods/query_record.html',querys=querys)

# 用户设置
from app.forms import User_Settings
@app.route('/user_settings/', methods=['GET', 'POST'])
@login_required
def user_settings():
    form = User_Settings()
    user = User.query.get(current_user.id)
    if form.validate_on_submit():
        user.now_num = form.now_num.data
        user.locker_distance = form.locker_distance.data
        user.maxlockernum = form.maxlockernum.data
        db.session.add(user)
        db.session.commit()
        flash("init ok!!")
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.now_num.data = user.now_num
        form.locker_distance.data = user.locker_distance
        form.maxlockernum.data = user.maxlockernum
    return render_template('/user_settings.html',form=form)