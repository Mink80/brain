# Brain!
# Copyright (C) Kai Sassmannshausen - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Kai Sassmannshausen <kai@sassie.de>, October 2019

# Imports
import os
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate # pip install Flask-Migrate
from forms import TaskForm
from enum import Enum
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# Forms config
app.config['SECRET_KEY'] = 'foobar'

# DB Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,"data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# for DB Migration
# before running migrations execute in cmd.exe:
# set FLASK_APP=brain.py
# flask db init
# flask db migrate -m "commit message"
# flask db upgrade
Migrate(app, db)

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

# Routes
@app.route('/')
def index():
    return render_template("home.html")


@app.route('/tasks', methods=['GET','POST'])
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        #session['name'] = form.name.data
        #session['weekly_relevant'] = form.weekly_relevant.data
        #session['customer_select'] = form.customer_select.data
        #session['info'] = form.info.data
        flash('you clicked submit')
        return redirect(url_for('tasks'))

    return render_template('tasks.html', form=form)

@app.route('/task_added')
def task_added():
    return render_template('task_added.html')

@app.route('/customers')
def customers():
    foo = "bar"
    mycustomers = ["BMW", "VW", "Daimler"]
    return render_template("customers.html",my_var=foo, customers=mycustomers)

@app.route('/add_customer', methods=['GET','POST'])
def add_customer():
    name = False
    form = TaskForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template("add_customer.html", form=form, name=name)

@app.route('/thank_you')
def thank_you():
    custname = request.args.get('custname')
    return render_template("thank_you.html", custname=custname)

@app.route('/customer/<name>')
def customer(name):
    return "<h1>Customer view: {}</h1>".format(name)

@app.route('/weekly')
def weekly():
    return render_template("weekly.html")


@app.route('/debug/<name>')
def debug(name):
    return name[100]

@app.errorhandler(404)
def page_not_found(e):
    # Last argument is the error code given to the browser
    return render_template('404.html'), 404

# Run this
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
