from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectField
from wtforms.validators import Length, DataRequired, Email, EqualTo
from flask_ckeditor import CKEditorField


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=30)], render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Retype Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')], render_kw={"placeholder": "Retype Password"})
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username or Email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


class ConsentForm(FlaskForm):
    consent = RadioField('', validators=[DataRequired()], choices=['Yes', 'No'])
    submit = SubmitField('Submit')


class Questionnaire(FlaskForm):
    question = RadioField('', validators=[DataRequired()], coerce=str)
    submit = SubmitField('Next')


class AgeGroup(FlaskForm):
    agegroups = RadioField('', choices=['5 - 17', '18 - 24', '25 - 34', '35 - 44', '45 - 54', '55 - 64', '65 - 74', '75+'])
    submit = SubmitField('Start')


class ChooseTable(FlaskForm):
    table = SelectField('', coerce=str)
    submit = SubmitField('Download')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Name"})
    email = StringField('Email Address', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    phone = StringField('Phone Number', render_kw={"placeholder": "Phone Number"})
    message = CKEditorField('Message', validators=[DataRequired()], render_kw={"placeholder": "Message"})
    submit = SubmitField('Submit')
