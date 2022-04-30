from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField


class AnswerForm(FlaskForm):
    content = TextAreaField('Введите ответ')
    submit = SubmitField('Применить')