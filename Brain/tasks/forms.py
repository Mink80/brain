#    Brain!
#    A lightweight web-application for managing tasks in projects
#
#    Copyright 2019, Kai Sassmannshausen
#    Source code repository: https://github.com/Mink80/brain
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
