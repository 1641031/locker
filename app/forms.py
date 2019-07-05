from flask_wtf import FlaskForm
#引入4种类型字段
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField,SelectField

#引入更新数据库信息的下拉表单
from wtforms.ext.sqlalchemy.fields import QuerySelectField
#表单的验证器
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

# app/models.py --User类
from app.models import User,Locker,Category,Goods


#登录用户表单
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


#注册用户表单
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        # 表单验证，请使用不同的用户名
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        # 表单验证，请使用不同的邮件名
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')




#储物柜的信息注册表单
class CreateLocker(FlaskForm):
    lockername = StringField('Lockername', validators=[DataRequired()])
    lockernumber = StringField('Lockernumber', validators=[DataRequired()])
    about_locker = TextAreaField('About Locker', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

#查看储物柜的详细信息表单
# class LockerInformation(FlaskForm):
    

#编辑储物柜详细信息的表单(改数据)
class EditLocker(FlaskForm):
    lockername = StringField('Lockername', validators=[DataRequired()])
    lockernumber = StringField('Lockernumber', validators=[DataRequired()])
    about_locker = TextAreaField('About Locker', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

#删除储物柜
class DeleteLocker(FlaskForm):
    lockername = StringField('Lockername', validators=[DataRequired()])
    submit = SubmitField('Submit')

#添加分类标签
class CreateCategory(FlaskForm):
    name = StringField('Lockername', validators=[DataRequired()])
    submit = SubmitField('Submit')

#编辑分类标签
class EditCategory(FlaskForm):
    name = StringField('CategoryName', validators=[DataRequired()])
    submit = SubmitField('Submit')

#删除分类标签
class DeleteCategory(FlaskForm):
    name = StringField('Categoryname', validators=[DataRequired()])
    submit = SubmitField('Submit')

#登录物品信息
class Login_Goods(FlaskForm):
    def query_locker():
        return Locker.query.all()
    def query_category():
        return Category.query.all()

    goodsname = StringField('Goodsname', validators=[DataRequired()])
    if Locker.query.all():
        locker = QuerySelectField(u'locker', query_factory=query_locker, get_label='lockername',allow_blank=True)
    if Category.query.all():
        category = QuerySelectField(u'category', query_factory=query_category, get_label='name',allow_blank=True)
    about_goods = TextAreaField('About Goods', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

#编辑物品名称
class Edit_Goods(FlaskForm):
    def query_locker():
        return Locker.query.all()
    def query_category():
        return Category.query.all()
    goodsname = StringField('Goodsname', validators=[DataRequired()])
    if Locker.query.all():
        locker = QuerySelectField(u'locker', query_factory=query_locker, get_label='lockername',allow_blank=True)
    if Category.query.all():
        category = QuerySelectField(u'category', query_factory=query_category, get_label='name',allow_blank=True)
    about_goods = TextAreaField('About Goods', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

#删除物品
class Delete_Goods(FlaskForm):
    goodsname = StringField('Goodsname', validators=[DataRequired()])
    submit = SubmitField('Submit')

#物品视图界面
class GoodsView(FlaskForm):
    goodsname = StringField('Goodsname', validators=[DataRequired()])