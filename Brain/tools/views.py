from flask import Blueprint, render_template, url_for
from Brain.models import HistoryItem, Task
from Brain.types import Weekly
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import re

tools_blueprint = Blueprint('tools',__name__,
                            template_folder='templates')


def get_start_and_end_date_from_calendar_week(year, calendar_week):
    monday = datetime.strptime(f'{year}-{calendar_week-1}-1', "%Y-%W-%w").date()
    return monday, monday + timedelta(days=6.9)

def weeks_for_year(year):
    # 04 Jan is per definition in the 1st week, makes 28th of Dec a day of the last week of a year
    last_week = date(year, 12, 28)
    # [1] is the number of week
    return last_week.isocalendar()[1]

def number_of_next_week(date):
    return (date + relativedelta(days=7)).isocalendar()[1]

def year_of_next_week(date):
    if number_of_next_week(date) > 50 and int((date + timedelta(days=7)).month == 1):
        return date.year
    return (date + timedelta(days=7)).year

def number_of_prev_week(date):
    return (date - timedelta(days=7)).isocalendar()[1]

def year_of_prev_week(date):
    return (date - timedelta(days=7)).year


@tools_blueprint.route('/history')
def history():
    history_items = HistoryItem.query.order_by(HistoryItem.id.desc()).limit(25).all()
    return render_template('/tools/history.html', history_items=history_items)


@tools_blueprint.route('weekly', defaults={'week': None, 'year': None},
                                methods=['GET','POST'])
@tools_blueprint.route('weekly/<year>/<week>', methods=['GET','POST'])
def weekly(year, week):
    max_weeks = 0

    # check for valid year and week.
    if not week or not year:
        week = datetime.now().isocalendar()[1]
        year = date.today().year
        max_weeks = weeks_for_year(year)
    else:
        if isinstance(week, str) and re.search("^\d{1,2}$", week) and \
            isinstance(year, str) and re.search("^\d{4}$", year):
                week = int(week)
                year = int(year)
                max_weeks = weeks_for_year(year)
                if not (week >= 1 and week <= max_weeks) or \
                    not (year >= 2019 and year <= (date.today() + relativedelta(years=1)).year):
                    # wrong week input
                    return render_template('400.html'), 400
        else:
            # wrong year/week input
            return render_template('400.html'), 400

    first_day, last_day = get_start_and_end_date_from_calendar_week(year, week)

    # "between" just includes the left side (first_day), so we add 1day to include last_day
    last_day_plus1 = last_day + timedelta(days=1)

    highlights = Task.query.filter(Task.last_change.between(first_day, last_day_plus1)). \
                            filter_by(weekly=Weekly.Highlight). \
                            filter_by(deleted=False). \
                            all()

    lowlights = Task.query.filter(Task.last_change.between(first_day, last_day_plus1)). \
                            filter_by(weekly=Weekly.Lowlight). \
                            filter_by(deleted=False). \
                            all()

    general = Task.query.filter(Task.last_change.between(first_day, last_day_plus1)). \
                            filter_by(weekly=Weekly.General). \
                            filter_by(deleted=False). \
                            all()

    upcoming = Task.query.filter(Task.last_change.between(first_day, last_day_plus1)). \
                            filter_by(weekly=Weekly.Upcoming). \
                            filter_by(deleted=False). \
                            all()

    prev_url = url_for('tools.weekly', year=year_of_prev_week(last_day),
                                        week=number_of_prev_week(last_day))

    next_url = url_for('tools.weekly', year=year_of_next_week(last_day),
                                        week=number_of_next_week(last_day))

    return render_template('/tools/weekly.html', week=week,
                                                year=year,
                                                max_weeks=max_weeks,
                                                max_year=datetime.now().year+1,
                                                next_url=next_url,
                                                prev_url=prev_url,
                                                first_day=first_day,
                                                last_day=last_day,
                                                highlights=highlights,
                                                lowlights=lowlights,
                                                general=general,
                                                upcoming=upcoming,)
