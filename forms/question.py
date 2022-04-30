from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField


class QuestionForm(FlaskForm):
    title = StringField('Вопрос (кратко)')
    content = TextAreaField('Вопрос (подробно)')
    submit = SubmitField('Применить')