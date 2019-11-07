import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_datepicker import datepicker
from datetime import date
import logging
from cryptography.fernet import Fernet

app = Flask(__name__)

# logging DEBUG
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

# Forms config
app.config['SECRET_KEY'] = 'foobar'
basedir = os.path.abspath(os.path.dirname(__file__))
dbdir = os.path.join(basedir, "database")

# DB Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(dbdir,"data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# for DB Migration
# before running migrations execute in cmd.exe:
# set FLASK_APP=brain.py
# flask db init
# flask db migrate -m "commit message"
# flask db upgrade
Migrate(app, db)

# See Documentation: https://github.com/mrf345/flask_datepicker/
datepicker(app)

# my jinja filters
def short_date(longdate):
    return(longdate.strftime("%d.%m.%y"))

app.jinja_env.filters['shortdate'] = short_date

# cryptography key generation
key = Fernet.generate_key()
crypter = Fernet(key)

# flask blueprints
from Brain.tasks.views import tasks_blueprint
from Brain.customers.views import customers_blueprint
from Brain.partners.views import partners_blueprint
from Brain.projects.views import projects_blueprint

app.register_blueprint(tasks_blueprint, url_prefix='/tasks')
app.register_blueprint(customers_blueprint, url_prefix='/customers')
app.register_blueprint(partners_blueprint, url_prefix="/partners")
app.register_blueprint(projects_blueprint, url_prefix="/projects")
