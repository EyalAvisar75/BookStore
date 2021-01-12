from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import Reader


class RegistrationForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_name(self, name):
        reader = Reader.query.filter_by(name=name.data).first()
        if reader:
            raise ValidationError('username already exists')
        return True

    def validate_email(self, email):
        reader = Reader.query.filter_by(email=email.data).first()
        if reader:
            raise ValidationError('email already exists')
        return True


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_name(self, name):
        if name.data != current_user.name:
            reader = Reader.query.filter_by(name=name.data).first()
            if reader:
                raise ValidationError('username already exists')
        return True

    def validate_email(self, email):
        if email.data != current_user.email:
            reader = Reader.query.filter_by(email=email.data).first()
            if reader:
                raise ValidationError('email already exists')
        return True


class RequestResetForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        reader = Reader.query.filter_by(email=email.data).first()
        if reader == None:
            raise ValidationError('There is no account with that email')
        return True


class ResetPasswordForm(FlaskForm):
    password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Reset Password')



