from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/customers')
def customers():
    foo = "bar"
    mycustomers = ["BMW", "VW", "Daimler"]
    return render_template("customers.html",my_var=foo, customers=mycustomers)

@app.route('/add_customer')
def add_customer():
    return render_template("add_customer.html")

@app.route('/thank_you')
def thank_you():
    custname = request.args.get('custname')
    return render_template("thank_you.html", custname=custname)

@app.route('/customer/<name>')
def customer(name):
    return "<h1>Customer view: {}</h1>".format(name)

@app.route('/debug/<name>')
def debug(name):
    return name[100]

@app.errorhandler(404)
def page_not_found(e):
    # Last argument is the error code given to the browser
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
