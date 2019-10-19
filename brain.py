from Brain import app
from flask import render_template

@app.route('/')
def index():
    return render_template('home.html')

@app.errorhandler(404)
def page_not_found(e):
    # Last argument is the error code given to the browser
    return render_template('404.html'), 404

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=80)
