from flask import Blueprint, render_template, redirect, url_for, flash
from Brain import db
from Brain.lib import delete_customer_from_db
from Brain.models import Customer, Project, Task
from Brain.customers.forms import CustomerForm, ConfirmDelete, CancelDelete
from Brain.projects.forms import ProjectForm


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

        flash('Customer added', 'alert alert-success alert-dismissible fade show')
        return redirect(url_for('customers.index'))

    return render_template("customers/list.html", customers=all_customers, form=form)


@customers_blueprint.route('/customer/<customer_id>', methods=['GET', 'POST'])
def customer(customer_id):
    form = ProjectForm()
    form.customer.choices = [(c.id, c.name) for c in Customer.query.all()]

    if form.validate_on_submit():
        db.session.add(Project(name=form.name.data,
                                customer_id=form.customer.data))
        db.session.commit()

        flash('Project added', 'alert alert-success alert-dismissible fade show')
        return redirect(url_for('customers.customer', customer_id=customer_id))

    customer=Customer.query.get(customer_id)
    # we need to use a dict as projects here because the project_table template expects this form
    projects = {}
    projects[customer] = Project.query.filter_by(customer_id=customer_id).all()

    return render_template('customers/customer.html',
                            projects=projects,
                            customer=customer,
                            form=form)


@customers_blueprint.route('/edit/<customer_id>', methods=['GET', 'POST'])
def edit(customer_id):
    customer_to_edit = Customer.query.get(customer_id)
    if not customer_to_edit:
        flash('Editing customer failed: No such customer', 'alert alert-danger alert-dismissible fade show')
        return redirect(url_for('customers.index'))

    form = CustomerForm(name=customer_to_edit.name,
                        comment=customer_to_edit.comment,
                        edit_id=customer_to_edit.id)

    form.submit.label.text = "Save"

    if form.validate_on_submit():
        customer_to_edit.name = form.name.data
        customer_to_edit.comment = form.comment.data

        db.session.add(customer_to_edit)
        db.session.commit()

        flash('Customer saved', 'alert alert-success alert-dismissible fade show')
        return redirect(url_for('customers.index'))

    else:
        customers = Customer.query.all()
        return render_template('/customers/edit.html', form=form,
                                                        edit_id=customer_to_edit.id,
                                                        customers=customers)


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
        if delete_customer_from_db(to_delete):
            flash('Customer deleted', 'alert alert-danger alert-dismissible fade show')
            return redirect(url_for('customers.index'))
        else:
            return render_template('400.html'), 400

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
                                                                no_actions_in_projcttable=True,
                                                                customer=to_delete,
                                                                deleted_tasks=deleted_tasks,
                                                                confirm_delete=confirm_delete,
                                                                cancel_delete=cancel_delete )
    else:
        if execute_deletion(to_delete):
            flash('Customer deleted', 'alert alert-danger alert-dismissible fade show')
            return redirect(url_for('customers.index'))
