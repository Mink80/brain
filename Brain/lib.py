#    Brain!
#    A lightweight web-application for managing tasks in projects
#
#    Copyright 2019, Kai Sassmannshausen
#    Source code repository: https://github.com/Mink80/brain
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import url_for
from Brain import db, crypter
from Brain.models import Task, Project, HistoryItem, Type, Weekly, Operation, Model
from Brain.tasks.forms import TaskForm

# expects a crypted url in origin
def build_redirect_url(origin, alternative):
    if not origin or origin == "":
        return url_for(alternative)
    else:
        # internal server error will be triggert if referrer was user manipulated
        # error will be cryptography.fernet.InvalidToken
        return crypter.decrypt(origin.encode()).decode()


# crypts referrer
# if referrer is None or "", return ""
def crypt_referrer(referrer):
    # in case the url gets called by user input directly, referrer is None
    if not referrer:
        return ""
    else:
        # crypt the referrer
        return crypter.encrypt(referrer.encode()).decode()


def write_history(operation, model, entity_id, customer_name=None,
                    project_name=None, comment=None):
    history_item = HistoryItem(operation, model, entity_id, customer_name,
                                project_name, comment)
    db.session.add(history_item)
    db.session.commit()


def add_project_and_write_history(project_form):
    project = Project(name=project_form.name.data, customer_id=project_form.customer.data)
    db.session.add(project)
    db.session.commit()

    write_history(operation=Operation.Added,
                    model=Model.Project,
                    entity_id=project.id,
                    customer_name=project.customer_name(),
                    project_name=project.name,
                    comment=f"Added project '{project.name}' for customer '{project.customer_name()}'")


def delete_project_from_db(project):
    if not project:
        return False

    # delete all tasks of the project
    tasks = project.tasks.count()
    for t in project.tasks.all():
        db.session.delete(t)

    # delete project
    db.session.delete(project)

    # write changes to db
    db.session.commit()

    # return number of deleted tasks
    return tasks


def delete_customer_from_db(customer):
    # validate customer
    if not customer:
        return False

    projects = customer.projects.count()
    tasks = 0

    # delete projects
    for p in customer.projects.all():
        tasks += delete_project_from_db(p)

    # delete customer
    db.session.delete(customer)

    # commit to db
    db.session.commit()

    return [projects,tasks]


def write_log_and_delete_customer(customer):
    projects_and_tasks = delete_customer_from_db(customer)
    if projects_and_tasks:

        write_history(operation=Operation.Deleted,
                        model=Model.Customer,
                        entity_id=customer.id,
                        customer_name=customer.name,
                        project_name=None,
                        comment=f"Deleted customer '{customer.name}' with {projects_and_tasks[0]} projects and {projects_and_tasks[1]} tasks.")
        return True
    else:
        return False


# returns a string with changed fields separated with a space
def task_changed(task, taskform, duedate):
    if not task or not taskform:
        return False

    changed = ""

    if task.text != taskform.text.data:
        changed += "text "
    if task.project_id != taskform.project.data:
        changed += "project "
    if task.type != Type(taskform.type.data):
        changed += "type "
    if task.duedate != duedate:
        changed += "duedate "
    if task.weekly != Weekly(taskform.weekly.data):
        changed = changed + "weekly "

    return changed


def project_changes(project, project_info_form):
    if not project or not project_info_form:
        return False

    changes = ""
    if project.opp != int(project_info_form.opp_number.data):
        changes += "opp "

    if  not project.partner_id:
        partner_id = 0
    else:
        partner_id = int(project.partner_id)

    if partner_id != int(project_info_form.partner.data):
        changes += "partner "

    if project.notes != project_info_form.notes.data:
        changes += "notes"

    return changes


# returns a string with changed fields (name, partner)
# the renaming function includes a change partner option as well
def project_rename_changes(project, rename_form):
    if not project or not rename_form:
        return False

    changed = ""
    if project.name != rename_form.new_name:
        changed += "name "
    if project.partner != rename_form.partner.data:
        changed += "partner "
    return changed


def customer_changes(customer, customer_form):
    if not customer or not customer_form:
        return False

    changes = ""

    if customer.name != customer_form.name.data:
        changes += "name "

    if customer.comment != customer_form.comment.data:
        changes += "comment "

    return changes


def partner_changes(partner, partner_form):
    if not partner or not partner_form:
        return False

    changes = ""

    if partner.name != partner_form.name.data:
        changes += "name "
    if partner.comment != partner_form.comment.data:
        changes += "comment "

    return changes
