from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import Regexp

class TaskForm(FlaskForm):
    customer = SelectField(u'Customer', id='select_customer', coerce=int)
    text = StringField("TaskName", validators=[Regexp(regex='^.+$', message='You need to provide a text')],
                                    render_kw={"placeholder": "Task Description"})
    project = SelectField(u"Project", id='select_project', coerce=int)
    type = SelectField(u"Type", coerce=int)
    duedate = StringField("DueDate", validators=[
        Regexp(regex='^(\d{4}-\d{2}-\d{2})*$', message='Use date format: YYYY-MM-DD or leave date field bank')
    ])
    weekly = SelectField(u"Weekly", coerce=int)
    # referrer used to jump back to original page view after editing a task
    referrer = HiddenField()
    submit = SubmitField("Add")
