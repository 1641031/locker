from flask_wtf import FlaskForm
#引入4种类型字段
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
#表单的验证器
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

# app/models.py --User类
from app.models import User


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




#物品视图界面
class GoodsView(FlaskForm):
    goodsname = StringField('Goodsname', validators=[DataRequired()])



