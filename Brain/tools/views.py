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

from flask import Blueprint, render_template, url_for, request
from Brain.models import HistoryItem, Task
from Brain.types import Weekly
from Brain.lib import str_to_int, get_start_and_end_date_from_calendar_week, \
                            weeks_for_year, number_of_next_week, year_of_next_week, \
                            number_of_prev_week, year_of_prev_week
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import re

tools_blueprint = Blueprint('tools',__name__,
                            template_folder='templates')


@tools_blueprint.route('/search', methods=['POST', 'GET'])
def search():
    search_string = request.form.get('Search', "")

    tasks = Task.query.filter(Task.text.like("%{}%".format(search_string))).all()

    return render_template('/tools/search_results.html',
                            search_string=search_string,
                            tasks=tasks,
                            no_actions_in_tasktable=True)


@tools_blueprint.route('/history/', defaults={'page':"1"})
@tools_blueprint.route('/history/<page>')
def history(page):
    #TODO: settings?
    maxpages = 50
    items_per_page = 20

    page = str_to_int(page)
    if page and page > 0 and page <= maxpages:
        history_items = HistoryItem.query.order_by(HistoryItem.id.desc()). \
                                        paginate(page, items_per_page, False)

        return render_template('/tools/history.html', history_items=history_items.items,
                                                        page=page,
                                                        maxpages=maxpages,
                                                        items_per_page=items_per_page)
    else:
        return render_template('400.html'), 400


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
