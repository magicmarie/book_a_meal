""" run server on port 5000"""
from api import APP
from flask import render_template


@APP.route('/', methods=['GET'])
def index():
    return render_template('home.html')

if __name__ == "__main__":
    APP.run(debug=True)
