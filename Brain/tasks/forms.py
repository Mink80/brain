from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
#    all_customers = Customer.query.all()
    choices = [(1,2),(3,4)]
    #for c in all_customers:
    #    choices.append({c.id, c.name})

    customer_select = SelectField(u'Customer', choices=choices)
    text = StringField("TaskName", validators=[DataRequired()])
    #TODO: project (dynamic - depending on customer)
    ball = SelectField(u"Ball", choices=[("1","2"),("3","4")])
    duedate = StringField("DueDate")
    weekly = SelectField(u"Ball", choices=[("1","2"),("3","4")])

    submit = SubmitField("Save")
