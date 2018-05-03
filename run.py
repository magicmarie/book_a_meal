import os
# from app import create_app
from app import app
from app.api.views import *

if __name__ == '__main__':

    app.run(debug=True)
