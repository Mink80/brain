from Brain import db
from datetime import date, datetime, timedelta
from .types import *

# DB Models
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    # date of creation
    cdate = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.Enum(Type))
    duedate = db.Column(db.Date)
    parent = db.Column(db.Integer)
    weekly = db.Column(db.Enum(Weekly))
    deleted = db.Column(db.Boolean)
    deleted_at = db.Column(db.DateTime)
    last_change = db.Column(db.DateTime)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)

    def __init__(self, text, project_id, cdate=datetime.now(), type=Type.Info,
                duedate=None, parent=0, weekly=Weekly.No, deleted=False,
                deleted_at=None, last_change=datetime.now()):
        self.text = text
        self.cdate = cdate
        self.type = type
        self.duedate = duedate
        self.parent = parent
        self.weekly = weekly
        self.deleted = deleted
        self.deleted_at = deleted_at
        self.last_change = last_change
        self.project_id = project_id

    def __repr__(self):
        return f"TaskID: {self.id}, Text: {self.text}, CDate: {self.cdate}, Type: {self.type}, DueDate: {self.duedate}, Parent: {self.parent}, Weekly: {self.weekly}, Project: {self.project_id}"

    def customer_id(self):
        return(Project.query.get(self.project_id).customer_id)

    def customer_name(self):
        return(Customer.query.get(self.customer_id()).name)

    def project_name(self):
        return(Project.query.get(self.project_id).name)

    def is_late(self):
        if self.duedate:
            return(datetime.now().date() > self.duedate)
        return(False)

    def is_almost_late(self):
        if self.duedate:
            return(datetime.now().date() == self.duedate or
                    (datetime.now().date() + timedelta(days = 1)) == self.duedate)

    def bgcolor(self):
        if (self.type == Type.Request or self.type == Type.Task):
            if self.is_late():
                return("mistyrose")

            elif self.is_almost_late():
                return("lemonchiffon")

            elif (self.type == Type.Request):
                return("honeydew")

            else:
                # must be a Task
                return("lightcyan")

        # must be Info or something went wrong
        return("")


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    comment = db.Column(db.Text)
    #tasks = db.relationship('Task', backref='customer', lazy='dynamic')
    projects = db.relationship('Project', backref='customer', lazy='dynamic')

    def __init__(self, name, comment=""):
        self.name = name
        self.comment = comment

    def __repr__(self):
        return f"ID: {self.id}, Customer: {self.name}, Comment: {self.comment}"


class Partner(db.Model):
    __tablename__ = 'partners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    comment = db.Column(db.Text)
    projects = db.relationship('Project', backref='partner', lazy='dynamic')

    def __init__(self, name, comment=""):
        self.name = name
        self.comment = comment

    def __repr__(self):
        return f"Partner {self.name}"


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    opp = db.Column(db.Integer)
    notes = db.Column(db.Text)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    partner_id = db.Column(db.Integer, db.ForeignKey('partners.id'))
    tasks = db.relationship('Task', backref='project', lazy='dynamic')

    def __init__(self, name, opp=None, customer_id=None, partner_id=None):
        self.name = name
        self.opp = opp
        self.customer_id = customer_id
        self.partner_id = partner_id

    def customer_name(self):
        return(Customer.query.get(self.customer_id).name)

    def partner_name(self):
        return(Partner.query.get(self.partner_id).name)

    def infos(self):
        return(self.tasks.filter_by(type=Type.Info).filter_by(deleted=False).all())

    def open_tasks(self):
        return(self.tasks.filter_by(type=Type.Task).filter_by(deleted=False).all())

    def requests(self):
        return(self.tasks.filter_by(type=Type.Request).filter_by(deleted=False).all())

    def deleted_tasks(self):
        return(self.tasks.filter_by(deleted=True).all())

    def __repr__(self):
        return f"ProjectID: {self.id}, Name: {self.name}, OPP: {self.opp}, Customer: {self.customer_id}, Partner {self.partner_id}"


class HistoryItem(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.Enum(Operation), nullable=False)
    model = db.Column(db.Enum(Model), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)
    customer_name = db.Column(db.Text)
    project_name = db.Column(db.Text)
    comment = db.Column(db.Text)
    time = db.Column(db.DateTime)

    def __init__(self, operation, model, entity_id, customer_name=None,
                    project_name=None, comment=None):
        self.operation = operation
        self.model = model
        self.entity_id = entity_id
        self.customer_name = customer_name
        self.project_name = project_name
        self.comment = comment
        self.time = datetime.now()

    def __repr__(self):
        return f"Operation: {self.operation}, Model: {self.model}, Entity ID: {self.entity_id}, Time: {self.time}"
