from flask import Blueprint, render_template, redirect, url_for, flash
from Brain import db
from Brain.models import Task, Customer, Project, Partner, Type, Weekly
from Brain.tasks.forms import TaskForm
from Brain.tasks.views import build_task
from Brain.projects.forms import ProjectForm, ProjectInfoForm

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

    return render_template('/projects/list.html', projects=projects,
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
        if project_info_form.partner.data is not 0:
            project.partner_id = project_info_form.partner.data
        project.notes = project_info_form.notes.data
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('projects.project', project_id=project.id))

    return render_template('/projects/project.html', tasks=tasks,
                                                project_info_form=project_info_form,
                                                project=project,
                                                edit_info=True)
