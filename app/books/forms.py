from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FloatField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    author = StringField(validators=[DataRequired()])
    author = StringField(validators=[DataRequired()])
    summary = TextAreaField(validators=[DataRequired()])
    price = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Add Book')


class BookEditForm(BookForm):
    submit = SubmitField('Update')
