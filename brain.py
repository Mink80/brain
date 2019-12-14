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

from Brain import app
from flask import render_template

from Brain.models import Task, HistoryItem, Project, Customer, Partner
from sqlalchemy import or_
from Brain.types import Type

@app.route('/')
def index():
    tasks_urgent = Task.query.filter( or_(Task.type==Type.Task, Task.type==Type.Request)). \
                        filter_by(deleted=False). \
                        filter(Task.duedate!=None). \
                        order_by(Task.duedate). \
                        limit(5). \
                        all()

    tasks_oldest = Task.query.filter( or_(Task.type==Type.Task, Task.type==Type.Request)). \
                            filter_by(deleted=False). \
                            filter(Task.duedate==None). \
                            order_by(Task.cdate). \
                            limit(5). \
                            all()

    history_items = HistoryItem.query.order_by(HistoryItem.id.desc()).limit(5).all()

    tasks_count = Task.query.filter_by(deleted=False).count()
    # should "misc" projects be counted in? i let it in for now...
    projects_count = Project.query.count()
    customers_count = Customer.query.count()
    partners_count = Partner.query.count()

    open_tasks_count = Task.query.filter_by(deleted=False). \
                                    filter_by(type=Type.Task). \
                                    count()

    open_requests_count = Task.query.filter_by(deleted=False). \
                                    filter_by(type=Type.Request). \
                                    count()

    return render_template('home.html', tasks_urgent=tasks_urgent,
                                        tasks_oldest=tasks_oldest,
                                        history_items=history_items,
                                        short_history_table=True,
                                        tasks_count=tasks_count,
                                        projects_count=projects_count,
                                        customers_count=customers_count,
                                        partners_count=partners_count,
                                        open_tasks_count=open_tasks_count,
                                        open_requests_count=open_requests_count)

@app.errorhandler(404)
def page_not_found(e):
    # Last argument is the error code given to the browser
    return render_template('404.html'), 404

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=80)
