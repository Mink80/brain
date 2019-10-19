from flask import Blueprint, render_template, redirect, url_for
from Brain import db
from Brain.models import Partner

partners_blueprint = Blueprint('partners', __name__,
                            template_folder='templates')


@partners_blueprint.route('/', methods=['GET','POST'])
def index():
    all_partners = Partner.query.all()
    return render_template("partners.html", partners=all_partners)
