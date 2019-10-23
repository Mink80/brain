import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate # pip install Flask-Migrate
from flask_datepicker import datepicker

app = Flask(__name__)

# Forms config
app.config['SECRET_KEY'] = 'foobar'
basedir = os.path.abspath(os.path.dirname(__file__))

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

# See Documentation: https://github.com/mrf345/flask_datepicker/
datepicker(app)

from Brain.tasks.views import tasks_blueprint
from Brain.customers.views import customers_blueprint
from Brain.partners.views import partners_blueprint
from Brain.projects.views import projects_blueprint

app.register_blueprint(tasks_blueprint, url_prefix='/tasks')
app.register_blueprint(customers_blueprint, url_prefix='/customers')
app.register_blueprint(partners_blueprint, url_prefix="/partners")
app.register_blueprint(projects_blueprint, url_prefix="/projects")
