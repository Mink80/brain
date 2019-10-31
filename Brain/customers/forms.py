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
