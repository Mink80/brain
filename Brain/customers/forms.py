from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from Brain.models import Customer

class CustomerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "Customer Name"})

    def validate_name(form, field):
        if (Customer.query.filter_by(name=field.data).first()):
            raise ValidationError('A customer with that name already exists')

    comment = StringField("Comment", render_kw={"placeholder": "Comment (optional)"})
    submit = SubmitField("Add")


class ConfirmDelete(FlaskForm):
    confirm = SubmitField("Confirm delete")


class CancelDelete(FlaskForm):
    cancel = SubmitField("Cancel")
