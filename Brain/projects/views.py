from flask import Blueprint, render_template, redirect, url_for, flash
from Brain import db
from Brain.models import Task, Customer, Project, Type, Weekly
from Brain.tasks.forms import TaskForm
from Brain.tasks.views import build_task

projects_blueprint = Blueprint('projects', __name__,
                                template_folder='templates')


@projects_blueprint.route('/')
def index():
    all_customers = Customer.query.all()

    projects = {}
    for c in all_customers:
        projects[c] = Project.query.filter_by(customer_id=c.id).all()

    return render_template('/projects/list.html', projects=projects)


@projects_blueprint.route('/<project_id>', methods=['GET','POST'])
def project(project_id):

    tasks = Task.query.filter_by(project_id=project_id)
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

    return render_template('/projects/project.html', tasks=tasks, form=form, project=project)
