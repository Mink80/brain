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
from Brain.models import Partner
import re

class PartnerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()],
                                           render_kw={"placeholder": "Partner Name"})

    def validate_name(form, field):
        p = Partner.query.filter_by(name=field.data).first()

        # if a project with that name exists in the db
        if p:
            # validate user input
            # and are we in an editing process of the queried customer?
            if isinstance(form.edit_id.data, str) and \
                re.search("^\d+$", form.edit_id.data) and \
                p.id == int(form.edit_id.data):
                    # save exit without raising an validation error
                    pass
            else:
                raise ValidationError('A Partner with that name already exists')

    comment = StringField("Comment", render_kw={"placeholder": "Comment (optional)"})
    edit_id = HiddenField()
    submit = SubmitField("Save")
