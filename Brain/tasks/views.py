from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from Brain import db
from Brain.models import Task, Customer, Project, Ball, Weekly
from Brain.tasks.forms import TaskForm

tasks_blueprint = Blueprint('tasks', __name__,
                            template_folder='templates')


@tasks_blueprint.route('/', methods=['GET','POST'])
def index():
    form = TaskForm()
    form.customer.choices = [(c.id, c.name) for c in Customer.query.all()]
    form.ball.choices = [(b.value, b.name) for b in Ball]
    form.weekly.choices = [(w.value, w.name) for w in Weekly]
    form.project.choices = [(p.id, p.name) for p in Project.query.all()]

    all_tasks = Task.query.all()

    if form.validate_on_submit():
        #session['name'] = form.name.data
        #session['weekly_relevant'] = form.weekly_relevant.data
        #session['customer_select'] = form.customer_select.data
        #session['info'] = form.info.data
        flash('you clicked submit')
        return redirect(url_for('tasks.index'))

    return render_template('list.html', tasks=all_tasks, form=form)


@tasks_blueprint.route('/_get_projects')
def _get_projects():
    customer = request.args.get('customer')
    projects = [(p.id, p.name) for p in Project.query.filter_by(customer_id=customer).all()]
    return jsonify(projects)
