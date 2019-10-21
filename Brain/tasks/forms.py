from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from ..models import Customer


class TaskForm(FlaskForm):
    customer = SelectField(u'Customer', id='select_customer')
    text = StringField("TaskName", validators=[DataRequired()])
    #TODO: project (dynamic - depending on customer)
    project = SelectField(u"Project", id='select_project')
    ball = SelectField(u"Ball")
    duedate = StringField("DueDate")
    weekly = SelectField(u"Ball")
    submit = SubmitField("Add")
