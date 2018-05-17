
# from app import create_app
from app import app
from app.api.views import *
from flask import render_template


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')


if __name__ == '__main__':

    app.run(debug=True)
