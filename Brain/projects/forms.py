from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from Brain.models import Project

class ProjectForm(FlaskForm):
    customer = SelectField(u'Customer', coerce=int)
    name = StringField("Name", validators=[DataRequired()],
                                render_kw={"placeholder": "Project Name"})

    def validate_name(form, field):
        if (Project.query.filter_by(name=field.data). \
                            filter_by(customer_id=form.customer.data).first()):
            raise ValidationError('A project with that name already exists for this customer')

    submit = SubmitField("Add")


class ProjectInfoForm(FlaskForm):
    opp_number = TextField('Opportunity', render_kw={"placeholder": "Opp number"})
    partner = SelectField(u'Partner', coerce=int, )
    notes = TextAreaField()
    submit_project_info = SubmitField("Save")


class RenameForm(FlaskForm):
    new_name = TextField('New Name', validators=[DataRequired()])
    partner = SelectField(u'Partner', coerce=int)
    origin = HiddenField()
    submit_rename = SubmitField("Save")
