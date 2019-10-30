from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

class CustomerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "Customer Name"})
    comment = StringField("Comment", render_kw={"placeholder": "Comment (optional)"})
    submit = SubmitField("Add")

class ConfirmDelete(FlaskForm):
    confirm = SubmitField("Confirm delete")

class CancelDelete(FlaskForm):
    cancel = SubmitField("Cancel")
