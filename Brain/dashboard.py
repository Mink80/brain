from flask import render_template
from Brain.models import Task, Project, Customer, Partner, HistoryItem
from sqlalchemy import or_
from Brain.types import Type

def dashboard():
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
