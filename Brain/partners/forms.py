from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

class PartnerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()],
                                           render_kw={"placeholder": "Partner Name"})
    
    comment = StringField("Comment", render_kw={"placeholder": "Comment (optional)"})
    edit_id = HiddenField()
    submit = SubmitField("Add")

 
