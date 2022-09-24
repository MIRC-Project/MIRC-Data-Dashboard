# Database models
from app.models import User

# Helper Functions for Flask forms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

class Date(FlaskForm):      # NDT7 test date selector form
    year = StringField('Year', validators=[DataRequired()])
    month = StringField('Month', validators=[DataRequired()])
    day = StringField('Day', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Forum(FlaskForm):     # Forum creation form
    title = TextAreaField('Create a New Thread?', validators=[DataRequired(), Length(min=0, max=125)])
    submit = SubmitField('+')

class Comments(FlaskForm):  # Forum posts form
    body = TextAreaField('Create a New Post?', validators=[DataRequired(), Length(min=0, max=500)])
    submit = SubmitField('+')

class LoginForm(FlaskForm): # User login form
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):  # User registration form
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):  # Checks if a username is taken
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):        # Checks validity of email address format
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):   # Edit profile form
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    # EditProfileForm instance is created without the parent class (FlaskForm) when __init__ is called
    # super() instantiates the FlaskForm of the derived class (EditProfileForm) in the current instance
    # __init__ accepts the current username of the logged-in user
    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)                           # args and kwargs are FlaskForm parameters 
        self.original_username = original_username

    def validate_username(self, username):              # Checks if a username is taken
        if username.data != self.original_username:     # If username has changed
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:                        # If username field is not empty
                raise ValidationError('Please use a different username.')

class ResetPasswordRequestForm(FlaskForm):      # Password reset request form
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):             # Password reset form
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', 
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Request Password Reset')