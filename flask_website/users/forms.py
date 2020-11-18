from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_website.models import User

class RegistrationForm(FlaskForm):
    username = StringField(label = 'Username', validators = [DataRequired(), 
                                                             Length(min = 2, max = 15)])
    email = StringField(label = 'Email', validators = [DataRequired(), Email()])
    password = PasswordField(label = 'Password', 
                             validators = [DataRequired()])
    confirm_password = PasswordField(label = 'Confirm Password', 
                                     validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is already taken. Choose a different username')
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is already taken. Choose a different email')
    
class LoginForm(FlaskForm):
    email = StringField(label = 'Email', validators = [DataRequired(), Email()])
    password = PasswordField(label = 'Password', 
                             validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class UpdateAccountForm(FlaskForm):
    username = StringField(label = 'Username', validators = [DataRequired(), 
                                                             Length(min = 2, max = 15)])
    email = StringField(label = 'Email', validators = [DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('That username is already taken. Choose a different username')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('That email is already taken. Choose a different email')
                
class RequestResetForm(FlaskForm):
    email = StringField(label = 'Email', validators = [DataRequired(), Email()])
    submit = SubmitField(label = 'Request Password Reset')
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. Please register first.')
            
class ResetPasswordForm(FlaskForm):
    password = PasswordField(label = 'Password', 
                             validators = [DataRequired()])
    confirm_password = PasswordField(label = 'Confirm Password', 
                                     validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField(label = 'Reset Password')