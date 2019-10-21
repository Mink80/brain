from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Regexp
from ..models import Customer


class TaskForm(FlaskForm):
    customer = SelectField(u'Customer', id='select_customer', coerce=int)
    text = StringField("TaskName", validators=[DataRequired()])
    #TODO: project (dynamic - depending on customer)
    project = SelectField(u"Project", id='select_project', coerce=int)
    type = SelectField(u"Type", coerce=int)
    duedate = StringField("DueDate", validators=[
        Regexp(regex='^(\d{4}-\d{2}-\d{2})*$', message="Format: YYYY-MM-DD")
    ])
    weekly = SelectField(u"Weekly", coerce=int)
    submit = SubmitField("Add")
