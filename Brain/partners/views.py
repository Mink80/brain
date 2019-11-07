from flask import Blueprint, render_template, redirect, url_for, request, flash
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


@partners_blueprint.route('/edit/<partner_id>', methods=['POST', 'GET'])
def edit(partner_id):
    to_edit = Partner.query.get(partner_id)
    if not to_edit:
        return render_template('400.html'), 400

    form = PartnerForm(name=to_edit.name, comment=to_edit.comment,
                        edit_id=to_edit.id)

    if form.validate_on_submit():
        to_edit.name = form.name.data
        to_edit.comment = form.comment.data
        db.session.add(to_edit)
        db.session.commit()
        flash('Partner edited', 'alert alert-success alert-dismissible fade show')
        return redirect(url_for('partners.index'))

    partners = Partner.query.all()
    return render_template("/partners/list.html", edit_id=to_edit.id,
                                                    form=form,
                                                    partners=partners)


@partners_blueprint.route('/delete/<partner_id>', methods=['POST', 'GET'])
def delete(partner_id):
    to_delete = Partner.query.get(partner_id)
    if not to_delete:
        return render_template('400.html'), 400

    if to_delete.projects.count() == 0:
        db.session.delete(to_delete)
        db.session.commit()
    else:
        flash('This partners has assigned projects', 'alert alert-danger alert-dismissible fade show')

    return redirect(url_for('partners.index'))
