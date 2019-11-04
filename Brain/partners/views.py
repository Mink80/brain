from flask import Blueprint, render_template, redirect, url_for
from Brain import db
from Brain.models import Partner
from Brain.partners.forms import PartnerForm

partners_blueprint = Blueprint('partners', __name__,
                            template_folder='templates')


@partners_blueprint.route('/', methods=['GET','POST'])
def index():
    form = PartnerForm()
    all_partners = Partner.query.all()
    
    if form.validate_on_submit():
        partner = Partner(name=form.name.data,
                          comment=form.comment.data)
        db.session.add(partner)
        db.session.commit()
        return redirect(url_for('partners.index'))
    
    return render_template("/partners/list.html", partners=all_partners,
                                                   form=form)
