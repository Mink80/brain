from flask import Blueprint, render_template, redirect, url_for
from Brain import db
from Brain.models import Customer

customers_blueprint = Blueprint('customers', __name__,
                            template_folder='templates')


@customers_blueprint.route('/', methods=['GET','POST'])
def index():
    all_customers = Customer.query.all()
    return render_template("customers.html", customers=all_customers)
