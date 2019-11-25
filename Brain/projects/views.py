from flask import Blueprint, render_template, redirect, url_for, flash, request
from Brain import db
from Brain.lib import  build_redirect_url, crypt_referrer, delete_project_from_db
from Brain.models import Task, Customer, Project, Partner, Type, Weekly
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
        db.session.add(Project(name=form.name.data,
                                customer_id=form.customer.data))
        db.session.commit()

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
        db.session.add(build_task(form))
        db.session.commit()

        flash('Task added', 'alert alert-success alert-dismissible fade show')
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
        project.opp = project_info_form.opp_number.data
        # partner == 0 means "None", so no write into the database
        if project_info_form.partner.data != 0:
            project.partner_id = project_info_form.partner.data
        project.notes = project_info_form.notes.data
        db.session.add(project)
        db.session.commit()
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
        db.session.add(to_rename)
        db.session.commit()
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
        if delete_project_from_db(to_delete):
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
