from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length, Email
import email_validator
from .validate import strip_filter, nome_check, email_check, email_check_login, password_check_login
from wtforms.csrf.session import SessionCSRF
from datetime import timedelta


"""********        FORM       *******"""

""" La meta class per formare una lista di filtri da applicare ad entrambi i form. """
# Crea dei conflitti con alcuni campi dei form: il BooleanField non restituisce vero o falso,
# il field upload non funziona come dovrebbe.
class BaseForm(FlaskForm):
    class Meta:
        def bind_field(self, form, unbound_field, options):
            filters = unbound_field.kwargs.get('filters', [])
            if strip_filter not in filters:
                filters.append(strip_filter)
            return unbound_field.bind(form=form, filters=filters, **options)


class RegistraForm(BaseForm):
    nome = StringField('Name', validators=[InputRequired(message='Required field'),
           Length(max=25, message='Name cannot have more than 25 characters'), nome_check])
    email = EmailField('Email', validators=[InputRequired(message='Required field'),
        Length(max=35, message='Email cannot have more than 25 characters'),
        Email(message='Invalid email', check_deliverability=False), email_check])
    password = PasswordField('Password', validators=[InputRequired(message='Required field'),
        Length(min=8, message='Password should have at least 8 characters')])
    confirm_pass = PasswordField('Confirm your password', validators=[InputRequired
        (message='Required field'), EqualTo('password',
        message='Passwords fields should match')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', filters=[strip_filter], validators=[InputRequired(message='Required field'),
        email_check_login])
    password = PasswordField('Password', validators=[InputRequired(message='Required field'),
        DataRequired(message='Invalid password'), password_check_login])
    remember_me = BooleanField()
    submit = SubmitField('Login')
