from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from Brain import db, crypter
from Brain.models import Task, Customer, Project
from Brain.tasks.forms import TaskForm
from Brain.types import Type, Weekly, Model, Operation
from Brain.lib import task_changed, write_history
from datetime import date, datetime
from sqlalchemy import not_
import re
from cryptography.fernet import Fernet

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


def write_new_task_to_db(form):
    task = build_task(form)
    db.session.add(task)
    db.session.commit()
    write_history(operation=Operation.Added,
                    model=Model.Task,
                    entity_id=task.id,
                    customer_name=task.customer_name(),
                    project_name=task.project_name(),
                    comment=f"Added {task.type.name} for project '{task.project_name()}' of customer '{task.customer_name()}'")


@tasks_blueprint.route('/', methods=['GET','POST'])
def index():
    form = build_form()

    tasks = Task.query.filter_by(deleted=False).all()

    if form.validate_on_submit():
        write_new_task_to_db(form)
        flash('Task added', 'alert alert-success alert-dismissible fade show')
        return redirect(url_for('tasks.index'))

    return render_template('/tasks/list.html', tasks=tasks, form=form, headline="Tasks")


@tasks_blueprint.route('/open', methods=['GET','POST'])
def open():
    form = build_form()

    tasks = Task.query.filter_by(deleted=False). \
                                filter(not_(Task.type.like(Type.Info))).all()

    if form.validate_on_submit():
        write_new_task_to_db(form)
        flash('Task added', 'alert alert-success alert-dismissible fade show')
        return redirect(url_for('tasks.open'))

    return render_template('/tasks/list.html', tasks=tasks, form=form, headline="Open Tasks")


@tasks_blueprint.route('/done/<task_id>', methods=['POST', 'GET'])
def done(task_id):
    mark_done = Task.query.get(task_id)
    if mark_done:
        # save old type state
        oldstate = mark_done.type

        # change type from task or request to info
        mark_done.type = Type.Info
        mark_done.last_change = datetime.now()

        # commit to db
        db.session.add(mark_done)
        db.session.commit()

        # write to history db table
        write_history(operation=Operation.Changed,
                        model=Model.Task,
                        entity_id=mark_done.id,
                        customer_name=mark_done.customer_name(),
                        project_name=mark_done.project_name(),
                        comment=f"Marked {oldstate.name} of project '{mark_done.project_name()}' of the customer '{mark_done.customer_name()}' as done.")

        flash(f'{oldstate.name} marked done', 'alert alert-success alert-dismissible fade show')
        return redirect(request.referrer)
    else:
        return render_template('400.html'), 400


@tasks_blueprint.route('/delete/<task_id>')
def delete(task_id):
    to_delete = Task.query.get(task_id)
    if to_delete:
        to_delete.deleted = True
        to_delete.deleted_at = datetime.now()
        to_delete.last_change = datetime.now()
        db.session.add(to_delete)
        db.session.commit()

        write_history(operation=Operation.Deleted,
                        model=Model.Task,
                        entity_id=to_delete.id,
                        customer_name=to_delete.customer_name(),
                        project_name=to_delete.project_name(),
                        comment=f"Deleted {to_delete.type.name} of project '{to_delete.project_name()}' of the customer '{to_delete.customer_name()}'.")

        flash('Task deleted', 'alert alert-warning alert-dismissible fade show')
    else:
        flash('No such task', 'alert alert-danger alert-dismissible fade show')

    return redirect(request.referrer)


@tasks_blueprint.route('/trash')
def trash():
    trashed_tasks = Task.query.filter_by(deleted=True).all()
    return render_template('/tasks/trash.html', tasks=trashed_tasks)


def delete_from_db(task_id):
    task_to_shredd = Task.query.get(task_id)
    if task_to_shredd and task_to_shredd.deleted:
        db.session.delete(task_to_shredd)
        db.session.commit()
        write_history(operation=Operation.Shredded,
                        model=Model.Task,
                        entity_id=task_to_shredd.id,
                        customer_name=task_to_shredd.customer_name(),
                        project_name=task_to_shredd.project_name(),
                        comment=f"Shredded {task_to_shredd.type.name} of project '{task_to_shredd.project_name()}' of the customer '{task_to_shredd.customer_name()}'")
        return(True)
    return(False)


@tasks_blueprint.route('/shredd/<task_id>')
def shredd(task_id):
    if delete_from_db(task_id):
        flash('Task shredded', 'alert alert-warning alert-dismissible fade show')
    else:
        flash('Task not found or task not marked as deleted', 'alert alert-danger alert-dismissible fade show')
    return(redirect(url_for('tasks.trash')))


@tasks_blueprint.route('/undelete/<task_id>')
def undelete(task_id):
    to_undelete = Task.query.get(task_id)
    if to_undelete:
        to_undelete.deleted = False
        to_undelete.deleted_at = None
        to_undelete.last_change = datetime.now()
        db.session.add(to_undelete)
        db.session.commit()
        write_history(operation=Operation.Undeleted,
                        model=Model.Task,
                        entity_id=to_undelete.id,
                        customer_name=to_undelete.customer_name(),
                        project_name=to_undelete.project_name(),
                        comment=f"Undeleted {to_undelete.type.name} of project '{to_undelete.project_name()}' of customer: '{to_undelete.customer_name()}'")
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

        # gets back None if nothing changed, else returnes TaskChange[] (Enum)
        changed_items = task_changed(to_edit, form, duedate)
        print(changed_items)

        if changed_items and len(changed_items) > 1:
            to_edit.text = form.text.data
            to_edit.project_id = form.project.data
            to_edit.type = Type(form.type.data)
            to_edit.duedate = duedate
            to_edit.weekly = Weekly(form.weekly.data)
            to_edit.last_change = datetime.now()

            db.session.add(to_edit)
            db.session.commit()

            write_history(operation=Operation.Changed,
                            model=Model.Task,
                            entity_id=to_edit.id,
                            customer_name=to_edit.customer_name(),
                            project_name=to_edit.project_name(),
                            comment=f"Modified {to_edit.type.name} of project '{to_edit.project_name()}' of customer: '{to_edit.customer_name()}': {changed_items}changed.")

            flash(f'{to_edit.type.name} saved', 'alert alert-success alert-dismissible fade show')

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
