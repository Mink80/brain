from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from Brain import db
from Brain.models import Task, Customer, Project, Type, Weekly
from Brain.tasks.forms import TaskForm
from datetime import date, datetime
from sqlalchemy import not_
import re
from cryptography.fernet import Fernet
from Brain import crypter

tasks_blueprint = Blueprint('tasks', __name__,
                            template_folder='templates')

def build_form():
    form = TaskForm()
    form.customer.choices = [(c.id, c.name) for c in Customer.query.all()]
    form.type.choices = [(t.value, t.name) for t in Type]
    form.weekly.choices = [(w.value, w.name) for w in Weekly]
    form.project.choices = [(p.id, p.name) for p in Project.query.all()]
    return(form)


def build_task(form):
    if form.duedate.data:
        duedate = date.fromisoformat(form.duedate.data)
    else:
        duedate = None

    return Task(text=form.text.data,
                project_id=form.project.data,
                type=Type(form.type.data),
                duedate=duedate,
                weekly=Weekly(form.weekly.data))


@tasks_blueprint.route('/', methods=['GET','POST'])
def index():
    form = build_form()

    tasks = Task.query.filter_by(deleted=False).all()

    if form.validate_on_submit():
        db.session.add(build_task(form))
        db.session.commit()

        flash('Task added', 'alert alert-success alert-dismissible fade show')
        return redirect(url_for('tasks.index'))

    return render_template('/tasks/list.html', tasks=tasks, form=form, headline="Tasks")


@tasks_blueprint.route('/open', methods=['GET','POST'])
def open():
    form = build_form()

    tasks = Task.query.filter_by(deleted=False). \
                                filter(not_(Task.type.like(Type.Info))).all()

    if form.validate_on_submit():
        db.session.add(build_task(form))
        db.session.commit()

        flash('Task added', 'alert alert-success alert-dismissible fade show')
        return redirect(url_for('tasks.open'))

    return render_template('/tasks/list.html', tasks=tasks, form=form, headline="Open Tasks")


@tasks_blueprint.route('/done/<task_id>', methods=['POST', 'GET'])
def done(task_id):
    mark_done = Task.query.get(task_id)
    if mark_done:
        mark_done.type = Type.Info
        db.session.add(mark_done)
        db.session.commit()
        flash('Task marked done', 'alert alert-success alert-dismissible fade show')
        return redirect(request.referrer)
    else:
        return render_template('400.html'), 400


@tasks_blueprint.route('/delete/<task_id>')
def delete(task_id):
    to_delete = Task.query.get(task_id)
    if to_delete:
        to_delete.deleted = True
        to_delete.deleted_at = datetime.now()
        db.session.add(to_delete)
        db.session.commit()
        flash('Task deleted', 'alert alert-warning alert-dismissible fade show')
    else:
        flash('No such task', 'alert alert-danger alert-dismissible fade show')

    return redirect(url_for('tasks.index'))


@tasks_blueprint.route('/trash')
def trash():
    trashed_tasks = Task.query.filter_by(deleted=True).all()
    return render_template('/tasks/trash.html', tasks=trashed_tasks)


def delete_from_db(task_id):
    task_to_shredd = Task.query.get(task_id)
    if task_to_shredd:
        db.session.delete(task_to_shredd)
        db.session.commit()
        return(True)
    return(False)


@tasks_blueprint.route('/shredd/<task_id>')
def shredd(task_id):
    if delete_from_db(task_id):
        flash('Task shredded', 'alert alert-warning alert-dismissible fade show')
    return(redirect(url_for('tasks.trash')))


@tasks_blueprint.route('/undelete/<task_id>')
def undelete(task_id):
    to_delete = Task.query.get(task_id)
    if to_delete:
        to_delete.deleted = False
        to_delete.deleted_at = datetime.now()
        db.session.add(to_delete)
        db.session.commit()
        flash('Task undeleted', 'alert alert-success alert-dismissible fade show')
    else:
        flash('No such task', 'alert alert-danger alert-dismissible fade show')

    return redirect(url_for('tasks.index'))


@tasks_blueprint.route('/edit/<task_id>/', methods=['GET','POST'])
def edit(task_id):
    # get the task object for editing from the db
    to_edit = Task.query.get(task_id)

    # if no task was found, flash an error and redirect to the tasks list
    if not to_edit:
        flash('Editing request failed: No such task', 'alert alert-danger alert-dismissible fade show')
        return redirect(url_for('tasks.index'))

    # for security reasons, lets encrypt the referer that we will add as
    # hidden field into the form. prevents client side manipulation attempts.
    crypted_referrer = crypter.encrypt(request.referrer.encode())

    # build the form and use the task values as the forms default values
    form = TaskForm(customer=to_edit.customer_id(),
                    text=to_edit.text,
                    project=to_edit.project_id,
                    type=to_edit.type.value,
                    duedate=to_edit.duedate,
                    weekly=to_edit.weekly.value,
                    referrer=crypted_referrer.decode())

    # and add the valid options for the form
    form.customer.choices = [(c.id, c.name) for c in Customer.query.all()]
    form.type.choices = [(b.value, b.name) for b in Type]
    form.weekly.choices = [(w.value, w.name) for w in Weekly]
    form.project.choices = [(p.id, p.name) for p in Project.query.all()]
    form.submit.label.text = "Save"

    if form.validate_on_submit():
        if form.duedate.data:
            duedate = date.fromisoformat(form.duedate.data)
        else:
            duedate = None

        to_edit.text = form.text.data
        to_edit.project_id = form.project.data
        to_edit.type = Type(form.type.data)
        to_edit.duedate = duedate
        to_edit.weekly = Weekly(form.weekly.data)

        db.session.add(to_edit)
        db.session.commit()

        flash('Task saved', 'alert alert-success alert-dismissible fade show')
        return redirect(crypter.decrypt(form.referrer.data.encode()).decode())

    else:

        # lets get the referrer
        ref = request.referrer

        # and prepare an empty tasks object
        tasks = None

        # next, we match the referer against valid options and build the tasks query accordingly
        # Valid options for referrer:
        # tasks         : http://<HOST_or_IP>/tasks/
        # open tasks    : http://<HOST_or_IP>/tasks/open
        # project       : http://<HOST_or_IP>/projects/<project_id>

        if re.search("^https?://(.+)/tasks/$", ref):
            tasks = Task.query.filter_by(deleted=False)

        elif re.search("^https?://(.+)/tasks/open$", ref):
            tasks = Task.query.filter_by(deleted=False). \
                                filter(not_(Task.type.like(Type.Info)))

        else:
            match = re.search("^https?://(.+)/projects/(\d+)$", ref)
            if match:
                tasks = Task.query.filter_by(project_id=match.group(2)). \
                                    filter_by(deleted=False)

        # if tasks is still None, no regex matched, something was wrong with the referrer.
        if not tasks:
            return render_template('400.html'), 400

        return render_template('/tasks/edit.html', form=form,
                                                    tasks=tasks,
                                                    edit_id=to_edit.id,
                                                    headline="Edit Task")


@tasks_blueprint.route('/_get_projects')
def _get_projects():
    customer = request.args.get('customer')
    projects = [(p.id, p.name) for p in Project.query.filter_by(customer_id=customer).all()]
    return jsonify(projects)
