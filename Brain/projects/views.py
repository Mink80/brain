from flask import Blueprint, render_template, redirect, url_for, flash
from Brain import db
from Brain.models import Task, Customer, Project

projects_blueprint = Blueprint('projects', __name__,
                                template_folder='templates')



@projects_blueprint.route('/')
def index():
    projects = Project.query.all()
    return render_template('/projects/list.html', projects=projects)
