from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from Brain.models import Partner

class PartnerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()],
                                           render_kw={"placeholder": "Partner Name"})

    def validate_name(form, field):
        p = Partner.query.filter_by(name=field.data).first()
        if p and (not int(p.id) == int(form.edit_id.data)):
            raise ValidationError('A Partner with that name already exists')

    comment = StringField("Comment", render_kw={"placeholder": "Comment (optional)"})
    edit_id = HiddenField()
    submit = SubmitField("Save")
