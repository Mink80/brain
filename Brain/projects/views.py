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

from flask import Blueprint, render_template, redirect, url_for, flash, request
from Brain import db
from Brain.lib import  build_redirect_url, crypt_referrer, delete_project_from_db, \
                        write_history, project_rename_changes, project_changes, \
                        add_project_and_write_history
from Brain.models import Task, Customer, Project, Partner
from Brain.types import Type, Weekly, Model, Operation
from Brain.tasks.forms import TaskForm
from Brain.tasks.views import build_task
from Brain.projects.forms import ProjectForm, ProjectInfoForm, RenameForm, \
                                CancelDelete, ConfirmDelete
import re

projects_blueprint = Blueprint('projects', __name__,
                                template_folder='templates')



@projects_blueprint.route('/', methods=['GET','POST'])
def index():
    form = ProjectForm()
    form.customer.choices = [(c.id, c.name) for c in Customer.query.all()]

    if form.validate_on_submit():
        add_project_and_write_history(form)
        flash('Project added', 'alert alert-success alert-dismissible fade show')
        return redirect(url_for('projects.index'))

    all_customers = Customer.query.all()

    projects = {}
    for c in all_customers:
        projects[c] = Project.query.filter_by(customer_id=c.id).all()

    return render_template('/projects/list.html', headline="Projects",
                                                    projects=projects,
                                                    form=form)


@projects_blueprint.route('/<project_id>', methods=['GET','POST'])
def project(project_id):

    tasks = Task.query.filter_by(project_id=project_id). \
                        filter_by(deleted=False).all()

    project = Project.query.get(project_id)

    form = TaskForm(customer=project.customer_id,
                    project=project.id)

    form.customer.choices = [(c.id, c.name) for c in Customer.query.all()]
    form.type.choices = [(t.value, t.name) for t in Type]
    form.weekly.choices = [(w.value, w.name) for w in Weekly]
    form.project.choices = [(p.id, p.name) for p in Project.query.all()]

    if form.validate_on_submit():
        task = build_task(form)
        db.session.add(task)
        db.session.commit()
        write_history(operation=Operation.Added,
                        model=Model.Task,
                        entity_id=task.id,
                        customer_name=task.customer_name(),
                        project_name=task.project_name(),
                        comment=f"Added {task.type.name} for project '{task.project_name()}' of customer '{task.customer_name()}'")

        flash(f'{task.type.name} added', 'alert alert-success alert-dismissible fade show')
        return redirect(url_for('projects.project', project_id=project_id))

    return render_template('/projects/project.html', tasks=tasks,
                                                        form=form,
                                                        project=project,
                                                        edit_info=False)


@projects_blueprint.route('/edit/<project_id>', methods=['GET', 'POST'])
def edit(project_id):
    tasks = Task.query.filter_by(project_id=project_id). \
                        filter_by(deleted=False).all()

    project = Project.query.get(project_id)

    project_info_form = ProjectInfoForm(opp_number=project.opp,
                                            partner=project.partner_id,
                                            notes=project.notes)

    project_info_form.partner.choices = [(0, "None")]
    project_info_form.partner.choices.extend([(p.id, p.name) for p in Partner.query.all()])

    if project_info_form.validate_on_submit():

        changes = project_changes(project, project_info_form)

        if changes and len(changes) > 0:
            project.opp = project_info_form.opp_number.data

            if project_info_form.partner.data == 0:
                project.partner_id = None
            else:
                project.partner_id = project_info_form.partner.data

            project.notes = project_info_form.notes.data

            db.session.add(project)
            db.session.commit()

            write_history(operation=Operation.Changed,
                            model=Model.Project,
                            entity_id=project.id,
                            customer_name=project.customer_name(),
                            project_name=project.name,
                            comment=f"Changed project '{project.name}' of customer '{project.customer_name()}': {changes}")

        return redirect(url_for('projects.project', project_id=project.id))

    return render_template('/projects/project.html', tasks=tasks,
                                                no_actions_in_tasktable=True,
                                                project_info_form=project_info_form,
                                                project=project,
                                                edit_info=True)


@projects_blueprint.route('/rename/<project_id>', methods=['POST', 'GET'])
def rename(project_id):
    to_rename = Project.query.get(project_id)
    if not to_rename:
        return render_template('400.html'), 400

    form = RenameForm(new_name = to_rename.name,
                        partner = to_rename.partner_id,
                        origin = crypt_referrer(request.referrer))

    form.partner.choices = [(0, "None")]
    form.partner.choices.extend([(p.id, p.name) for p in Partner.query.all()])

    if form.validate_on_submit():
        to_rename.name = form.new_name.data
        if form.partner.data != 0:
            to_rename.partner_id = form.partner.data
        else:
            to_rename.partner_id = None
            form.partner.data = None

        changed = project_rename_changes(to_rename, form)

        if changed and len(changed) > 1:
            db.session.add(to_rename)
            db.session.commit()

            write_history(operation=Operation.Changed,
                            model=Model.Project,
                            entity_id=to_rename.id,
                            customer_name=to_rename.customer_name(),
                            project_name=to_rename.name,
                            comment=f"Changed project '{to_rename.name}' of customer '{to_rename.customer_name()}': {changed}")

            flash('Project edited', 'alert alert-success alert-dismissible fade show')
        return redirect(build_redirect_url(form.origin.data, 'projects.index'))

    all_customers = Customer.query.all()
    projects = {}
    for c in all_customers:
        projects[c] = Project.query.filter_by(customer_id=c.id).all()

    return render_template('/projects/list.html', headline=f"Edit Project {to_rename.name}",
                                                projects=projects,
                                                rename_id=to_rename.id,
                                                form=form)


@projects_blueprint.route('/delete/<project_id>', methods=['POST', 'GET'])
def delete(project_id):
    to_delete = Project.query.get(project_id)
    if not to_delete or to_delete.name == "Misc":
        return render_template('400.html'), 400

    ref = crypt_referrer(request.referrer)

    # build forms and fill in the crypted referrer (or "")
    confirm_delete = ConfirmDelete(origin=ref)
    cancel_delete = CancelDelete(origin=ref)

    # deletion was confirmed by user
    if confirm_delete.validate_on_submit() and confirm_delete.confirm.data:
        tasks = delete_project_from_db(to_delete)

        if tasks or tasks == 0:
            write_history(operation=Operation.Deleted,
                            model=Model.Project,
                            entity_id=to_delete.id,
                            customer_name=to_delete.customer_name(),
                            project_name=to_delete.name,
                            comment=f"Deleted project '{to_delete.name}' of customer '{to_delete.customer_name()}': {tasks} tasks deleted.")

            flash('Project deleted', 'alert alert-danger alert-dismissible fade show')
            return redirect(build_redirect_url(confirm_delete.origin.data, 'projects.index'))
        else:
            return render_template('400.html'), 400

    # deletion was canceled by user
    elif cancel_delete.validate_on_submit() and cancel_delete.cancel.data:
        return redirect(build_redirect_url(confirm_delete.origin.data, 'projects.index'))

    tasks = Task.query.filter_by(project_id=project_id). \
                        filter_by(deleted=False).all()

    # show confirm deletion page
    return render_template("/projects/project.html", project=to_delete,
                                                    edit_info=False,
                                                    delete_confirmation=True,
                                                    tasks=tasks,
                                                    no_actions_in_tasktable=True,
                                                    cancel_delete=cancel_delete,
                                                    confirm_delete=confirm_delete)
