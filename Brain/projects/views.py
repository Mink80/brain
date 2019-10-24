from flask import Blueprint, render_template, redirect, url_for, flash
from Brain import db
from Brain.models import Task, Customer, Project

projects_blueprint = Blueprint('projects', __name__,
                                template_folder='templates')



@projects_blueprint.route('/')
def index():
    all_customers = Customer.query.all()

    projects = {}
    for c in all_customers:
        projects[c] = Project.query.filter_by(customer_id=c.id).all()

    return render_template('/projects/list.html', projects=projects)


@projects_blueprint.route('/<project_id>')
def project(project_id):

    tasks = Task.query.filter_by(id=project_id)

    return render_template('/projects/project.html', tasks=tasks)
