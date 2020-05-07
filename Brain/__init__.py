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

# cryptography key generation
key = Fernet.generate_key()
crypter = Fernet(key)

# Forms config
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') \
    if os.getenv('SECRET_KEY') else key.decode()

# DB Config

# SQLite
#basedir = os.path.abspath(os.path.dirname(__file__))
#dbdir = os.path.join(basedir, "database")
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(dbdir,"data.sqlite")

# PostgreSQL
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://user:pass@dbhost/dbname'

# MySQL (there is an issue with mysql. it seems it does not like unique=True in db models)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:pass@dbhost/dbname'

# per environment
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# lets check if the db is working
try:
    # to check database we will execute raw query
    db.create_all()
    log.info("Database connected.")
except Exception as e:
    log.error("Error connecting with database.")

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

def short_time(longtime):
    return(longtime.strftime("%d.%m.%y - %H:%M"))

app.jinja_env.filters['shorttime'] = short_time

# cryptography key generation
key = Fernet.generate_key()
crypter = Fernet(key)

# flask blueprints
from Brain.tasks.views import tasks_blueprint
from Brain.customers.views import customers_blueprint
from Brain.partners.views import partners_blueprint
from Brain.projects.views import projects_blueprint
from Brain.tools.views import tools_blueprint

app.register_blueprint(tasks_blueprint, url_prefix='/tasks')
app.register_blueprint(customers_blueprint, url_prefix='/customers')
app.register_blueprint(partners_blueprint, url_prefix="/partners")
app.register_blueprint(projects_blueprint, url_prefix="/projects")
app.register_blueprint(tools_blueprint, url_prefix="/tools")
