from flask import Blueprint, render_template, redirect, url_for
from Brain import db
from Brain.models import Task
from Brain.tasks.forms import TaskForm

tasks_blueprint = Blueprint('tasks', __name__,
                            template_folder='templates')


@tasks_blueprint.route('/', methods=['GET','POST'])
def index():
    form = TaskForm()
    all_tasks = Task.query.all()

    if form.validate_on_submit():
        #session['name'] = form.name.data
        #session['weekly_relevant'] = form.weekly_relevant.data
        #session['customer_select'] = form.customer_select.data
        #session['info'] = form.info.data
        flash('you clicked submit')
        return redirect(url_for('tasks.index'))

    return render_template('list.html', tasks=all_tasks, form=form)
