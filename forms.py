from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo


class RegistrationForm(FlaskForm):
    username=StringField('UserName',
                         validators=[DataRequired(),Length(min=2,max=12)])    
    email=EmailField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=4,max=16)])
    confirm_password=PasswordField('ConfrimPassword',validators=[DataRequired(),Length(min=4,max=16),EqualTo('password')])
    submit=SubmitField('Sign Up')
    
    
class LoginForm(FlaskForm):
    
    email=EmailField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=4,max=16)])
    remember=BooleanField('remember me')
    submit=SubmitField('Login')
    
    
class PostForm(FlaskForm):
        title=StringField("Title",validators=[DataRequired()])
        content=TextAreaField("Content",validators=[DataRequired()])
        submit=SubmitField('Post')   
    