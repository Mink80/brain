from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from Brain import db
from Brain.models import Task, Customer, Project, Ball, Weekly
from Brain.tasks.forms import TaskForm
from datetime import date, datetime

tasks_blueprint = Blueprint('tasks', __name__,
                            template_folder='templates')


@tasks_blueprint.route('/', methods=['GET','POST'])
def index():
    form = TaskForm()
    form.customer.choices = [(c.id, c.name) for c in Customer.query.all()]
    form.ball.choices = [(b.value, b.name) for b in Ball]
    form.weekly.choices = [(w.value, w.name) for w in Weekly]
    form.project.choices = [(p.id, p.name) for p in Project.query.all()]

    all_tasks = Task.query.filter_by(deleted=False)

    if form.validate_on_submit():
        if form.duedate.data:
            duedate = date.fromisoformat(form.duedate.data)
        else:
            duedate = None

        new_task = Task(text=form.text.data,
                        project_id=form.project.data,
                        ball=Ball(form.ball.data),
                        duedate=duedate,
                        weekly=Weekly(form.weekly.data)
                        )
        db.session.add(new_task)
        db.session.commit()

        flash('Task added.', 'alert alert-success alert-dismissible fade show')
        return redirect(url_for('tasks.index'))

    return render_template('list.html', tasks=all_tasks, form=form)


@tasks_blueprint.route('/delete/<task_id>')
def delete(task_id):
    to_delete = Task.query.get(task_id)
    if to_delete:
        to_delete.deleted = True
        to_delete.deleted_at = datetime.now()
        db.session.add(to_delete)
        db.session.commit()
        flash('Task deleted.', 'alert alert-warning alert-dismissible fade show')
    else:
        flash('No such task.', 'alert alert-danger alert-dismissible fade show')

    return redirect(url_for('tasks.index'))


@tasks_blueprint.route('/_get_projects')
def _get_projects():
    customer = request.args.get('customer')
    projects = [(p.id, p.name) for p in Project.query.filter_by(customer_id=customer).all()]
    return jsonify(projects)
