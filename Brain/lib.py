from flask import url_for
from Brain import db, crypter
from Brain.models import Task, HistoryItem, Type, Weekly
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


def delete_project_from_db(project):
    if not project:
        return False

    # delete all tasks of the project
    for t in project.tasks.all():
        db.session.delete(t)

    # delete project_table
    db.session.delete(project)

    # write changes to db
    db.session.commit()

    return True


def delete_customer_from_db(customer):
    # validate customer
    if not customer:
        return False

    # delete projects
    for p in customer.projects.all():
        delete_project_from_db(p)

    # delete customer
    db.session.delete(customer)

    # commit to db
    db.session.commit()

    return(True)

# returns a string with changed fields separated with a space
def task_changed(task, taskform, duedate):
    if not task or not taskform:
        return False

    changed = ""

    if task.text != taskform.text.data:
        changed = changed + "text "
    if task.project_id != taskform.project.data:
        changed = changed + "project "
    if task.type != Type(taskform.type.data):
        changed = changed + "type "
    if task.duedate != duedate:
        changed = changed + "duedate "
    if task.weekly != Weekly(taskform.weekly.data):
        changed = changed + "weekly "

    return changed


def project_changed():
    pass


def customer_changed():
    pass


def partner_changed():
    pass
