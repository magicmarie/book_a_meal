""" run server on port 5000"""
from api import APP, DB
from flask import render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

# instance of the app in manager
manager = Manager(APP)

# instance of the app and db in migrate
migrate = Migrate(APP, DB)

manager.add_command('db', MigrateCommand)


@APP.route('/', methods=['GET'])
def index():
    return render_template('home.html')


if __name__ == "__main__":
    manager.run()
