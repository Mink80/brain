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
from Brain.models import Project

class ProjectForm(FlaskForm):
    customer = SelectField(u'Customer', coerce=int)
    name = StringField("Name", validators=[DataRequired()],
                                render_kw={"placeholder": "Project Name"})
    submit = SubmitField("Add")

    def validate_name(form, field):
        p = Project.query.filter_by(name=field.data). \
                            filter_by(customer_id=form.customer.data).first()
        if p:
            raise ValidationError('A project with that name already exists for this customer')


class ProjectInfoForm(FlaskForm):
    opp_number = StringField('Opportunity', render_kw={"placeholder": "Opp number"})
    partner = SelectField(u'Partner', coerce=int, )
    notes = TextAreaField(id="summernote")
    submit_project_info = SubmitField("Save")


class RenameForm(FlaskForm):
    new_name = StringField('New Name', validators=[DataRequired()])
    partner = SelectField(u'Partner', coerce=int)
    origin = HiddenField()
    edit_id = HiddenField()
    submit_rename = SubmitField("Save")

    def validate_name(form, field):
        p = Project.query.filter_by(name=field.data). \
                            filter_by(customer_id=form.customer.data).first()
        if p:
            # validate user input
            # and are we in an editing process of the queried customer?
            if isinstance(form.edit_id.data, str) and \
                re.search("^\d+$", form.edit_id.data) and \
                p.id == int(form.edit_id.data):
                    # save exit without raising an validation error
                    pass
            else:
                raise ValidationError('A project with that name already exists for this customer')


class ConfirmDelete(FlaskForm):
    origin = HiddenField()
    confirm = SubmitField("Confirm delete")

class CancelDelete(FlaskForm):
    origin = HiddenField()
    cancel = SubmitField("Cancel")
