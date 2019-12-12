#    Brain!
#    A lightweight web-application for managing tasks in projects
#
#    Copyright 2019, Kai Sassmannshausen
#    Source code repository: https://github.com/Mink80/brain
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Blueprint, render_template, redirect, url_for, request, flash
from Brain import db
from Brain.models import Partner, Operation, Model
from Brain.lib import write_history, partner_changes
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

        write_history(operation=Operation.Added,
                        model=Model.Partner,
                        entity_id=partner.id,
                        customer_name=None,
                        project_name=None,
                        comment=f"Added partner '{partner.name}'")

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
        changes = partner_changes(to_edit, form)

        if changes:
            to_edit.name = form.name.data
            to_edit.comment = form.comment.data
            db.session.add(to_edit)
            db.session.commit()

            write_history(operation=Operation.Changed,
                            model=Model.Partner,
                            entity_id=to_edit.id,
                            customer_name=None,
                            project_name=None,
                            comment=f"Changed partner '{to_edit.name}': {changes}")

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
        write_history(operation=Operation.Deleted,
                        model=Model.Partner,
                        entity_id=to_delete.id,
                        customer_name=None,
                        project_name=None,
                        comment=f"Deleted partner '{to_delete.name}'")

        flash('partner deleted', 'alert alert-warning alert-dismissible fade show')

    else:
        flash('This partners has assigned projects', 'alert alert-danger alert-dismissible fade show')

    return redirect(url_for('partners.index'))
