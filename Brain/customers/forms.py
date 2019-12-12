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
from wtforms.validators import DataRequired
from Brain.models import Customer

class CustomerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()],
                                render_kw={"placeholder": "Customer Name"})

    def validate_name(form, field):
        c = Customer.query.filter_by(name=field.data).first()
        if c and (not int(c.id) == int(form.edit_id.data)):
            raise ValidationError('A customer with that name already exists')

    comment = StringField("Comment", render_kw={"placeholder": "Comment (optional)"})
    # this is used by the validator above to check if we are in an editing process
    edit_id = HiddenField()
    submit = SubmitField("Add")


class ConfirmDelete(FlaskForm):
    confirm = SubmitField("Confirm delete")


class CancelDelete(FlaskForm):
    cancel = SubmitField("Cancel")
