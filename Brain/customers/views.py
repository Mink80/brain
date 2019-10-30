from flask import Blueprint, render_template, redirect, url_for, flash
from Brain import db
from Brain.models import Customer, Project, Task
from Brain.customers.forms import CustomerForm, ConfirmDelete, CancelDelete


customers_blueprint = Blueprint('customers', __name__,
                            template_folder='templates')


@customers_blueprint.route('/', methods=['GET','POST'])
def index():
    form = CustomerForm()
    all_customers = Customer.query.all()

    if form.validate_on_submit():
        # Create customer
        customer = Customer(name=form.name.data, comment=form.comment.data)
        db.session.add(customer)
        # Commit the customer to get an id
        db.session.commit()

        # Add "Misc" Project for the new customer and commit it as well
        project = Project(name="Misc", customer_id=customer.id)
        db.session.add(project)
        db.session.commit()

        return redirect(url_for('customers.index'))

    return render_template("customers/list.html", customers=all_customers, form=form)


@customers_blueprint.route('/customer/<customer_id>')
def customer(customer_id):
    customer=Customer.query.get(customer_id)
    # we need to use a dict as projects here because the project_table template expects this form
    projects = {}
    projects[customer] = Project.query.filter_by(customer_id=customer_id).all()

    print(projects)

    return render_template('customers/customer.html',
                            projects=projects,
                            customer=customer)


def execute_deletion(customer):
    # validate customer
    if customer:
        # get all projects
        projects_to_delete = customer.projects.all()

        # get all tasks
        tasks_to_delete = []
        for p in projects_to_delete:
            tasks_to_delete.extend(p.tasks.all())

        # delete tasks
        for t in tasks_to_delete:
            db.session.delete(t)

        # delete projects
        for p in projects_to_delete:
            db.session.delete(p)

        # delete customer
        db.session.delete(customer)

        # commit to db
        db.session.commit()

        return(True)

    return(False)


@customers_blueprint.route('/delete/<customer_id>', methods=['GET', 'POST'])
def delete(customer_id):
    # create Forms
    confirm_delete = ConfirmDelete()
    cancel_delete = CancelDelete()

    to_delete = Customer.query.get(customer_id)

    if not to_delete:
        flash('No such customer', 'alert alert-danger alert-dismissible fade show')
        return redirect(url_for('customers.index'))

    if confirm_delete.validate_on_submit() and confirm_delete.confirm.data:
        if execute_deletion(to_delete):
            flash('Customer deleted', 'alert alert-danger alert-dismissible fade show')
            return redirect(url_for('customers.index'))

    elif cancel_delete.validate_on_submit() and cancel_delete.cancel.data:
        return redirect(url_for("customers.index"))

    # check if projects and tasks exists before deleting the customer
    # we need to use a dict as projects here because the project_table template expects this form
    projects = {}
    projects[to_delete] = Project.query.filter_by(customer_id=to_delete.id).all()

    # count the deleted and non-deleted tasks
    tasks = []
    deleted_tasks = 0
    for p in projects[to_delete]:
        tasks.extend(p.tasks.filter_by(deleted=False).all())
        deleted_tasks += len(p.tasks.filter_by(deleted=True).all())

    if (len(projects) > 1 or len(tasks) > 0):
        return render_template("/customers/confirm_delete.html", projects=projects,
                                                                customer=to_delete,
                                                                deleted_tasks=deleted_tasks,
                                                                confirm_delete=confirm_delete,
                                                                cancel_delete=cancel_delete )
    else:
        if execute_deletion(to_delete):
            flash('Customer deleted', 'alert alert-danger alert-dismissible fade show')
            return redirect(url_for('customers.index'))
