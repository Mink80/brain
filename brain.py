#    Brain!
#    A lightweight web-application for managing tasks in projects
#
#    Copyright 2019, Kai Sassmannshausen
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
from flask import render_template, request
from Brain.models import Task

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    search_string = request.form.get('Search', "")

    tasks = Task.query.filter(Task.text.like("%{}%".format(search_string))).all()

    return render_template('search_results.html',
                            search_string=search_string,
                            tasks=tasks)

@app.errorhandler(404)
def page_not_found(e):
    # Last argument is the error code given to the browser
    return render_template('404.html'), 404

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=80)
