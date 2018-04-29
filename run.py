import os
# from app import create_app
from app.api import app
from app.api.views import *

if __name__ == '__main__':

    app.run(debug=True)
