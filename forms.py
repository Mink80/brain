from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    name = StringField("TaskName", validators=[DataRequired()])
    weekly_relevant = BooleanField("Weekly relevant")
    customer_select = SelectField(u'Customer',
                                    choices=[
                                            ('bmw','BMW'),
                                            ('int','internal'),
                                            ('saba','SABA')
                                            ])
    info = TextAreaField("Info")
    submit = SubmitField("Save")
