from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    title = StringField('Описание работы', validators=[DataRequired()])
    work_size = IntegerField('Описание работы', validators=[DataRequired()])
    collaborators = StringField('Соисполнители')
    start_date = DateField('Дата начала')
    end_date = DateField('Дата завершения')
    is_finished = BooleanField('Завершено')
    submit = SubmitField('Добавить')
