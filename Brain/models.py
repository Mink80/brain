from Brain import db
from enum import Enum
import datetime

# Enums
class Ball(Enum):
    Any = 0
    Mine = 1
    Others = 2

class Weekly(Enum):
    No = 0
    Highlight = 1
    Lowlight = 2
    General = 3
    Upcoming = 4

# DB Models
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    cdate = db.Column(db.DateTime, nullable=False)
    ball = db.Column(db.Enum(Ball))
    duedate = db.Column(db.Date)
    parent = db.Column(db.Integer)
    weekly = db.Column(db.Enum(Weekly))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, text, cdate=datetime.datetime.now(), ball=Ball.Any,
                duedate=datetime.datetime.min, parent=0, weekly=Weekly.No,
                customer_id=None, project_id=None):
        self.text = text
        self.cdate = cdate
        self.ball = ball
        self.duedate = duedate
        self.parent = parent
        self.weekly = weekly
        self.customer_id = customer_id
        self.project_id = project_id

    def __repr__(self):
        return f"TaskID: {self.id}, Text: {self.text}, CDate: {self.cdate}, Ball: {self.ball}, DueDate: {self.duedate}, Parent: {self.parent}, Weekly: {self.weekly}, Customer: {self.customer_id}, Prject: {self.project_id}"

    def customer_name(self):
        return(Customer.query.get(self.customer_id).name)

    def project_name(self):
        return(Project.query.get(self.project_id).name)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    comment = db.Column(db.Text)
    tasks = db.relationship('Task', backref='customer', lazy='dynamic')
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
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    partner_id = db.Column(db.Integer, db.ForeignKey('partners.id'))
    tasks = db.relationship('Task', backref='project', lazy='dynamic')

    def __init__(self, name, opp=0, customer_id=None, partner_id=None):
        self.name = name
        self.opp = opp
        self.customer_id = customer_id
        self.partner_id = partner_id

    def __repr__(self):
        return f"ProjectID: {self.id}, Name: {self.name}, OPP: {self.opp}, Customer: {self.customer_id}, Partner {self.partner_id}"
