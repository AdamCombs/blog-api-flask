from flask import Flask
from .extensions import jwt
from .extensions import db
import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from application.models.user_table import User
from application.models.blog_table import Blog
from application.models.tag_table import Tag
from application.models.tag_blog_relationship_table import *
from application.config import *

# The following commands for running Flask with Debug mode ON
# In terminal with venv activated enter: (with NO spaces around the '=' signs)
# set FLASK_ENV=development
# The following debug variable is set automatically in the 'load application config from object section'
# set FLASK_DEBUG=1

# Then you can run with the following command
# flask run

# From venv in terminal the following commands for creating the SQLAlchemy databases
# Note: the database models must be imported into the application.__init__.py file
# In terminal enter:
# python
# from application.__init__ import create_app
# from application.extensions import db
# db.create_all(application=create_app())
# exit()

# The requirements document is created and can automatically be updated via the following command with venv active
# pip freeze > requirements.txt


def create_app():
    app = Flask(__name__)

    # Chooses set of environment variables based on object located within config file
    app.config.from_object(config.DevelopmentConfig)
    # application.config.from_object(config.ProductionConfig)
    # application.config.from_object(config.TestingConfig)

    # Register methods to prevent circular dependencies
    # Everything must take place in it's proper order
    register_extensions(app)
    register_blueprints(app)

    # Add a command line command to create the admin user with username and password
    # This CLI command adds a user to the database with the below username and password
    create_first_user(app)

    return app

def register_extensions(app):
    # Registers the extensions with the current application
    jwt.init_app(app)
    db.init_app(app)
    return None

def register_blueprints(app):
    # Registers the blueprints with the current application
    from . import public_views
    app.register_blueprint(public_views.public_views)

    from . import private_views
    app.register_blueprint(private_views.private_views)
    return None

def create_first_user(app):
    @click.command(name='create_admin')
    @with_appcontext
    def create_admin():
        username='adamcombs1'
        password='D0peB@ss'
        password_hashed = generate_password_hash(password, 'sha256', salt_length=12)
        user_to_add = User(username=username, password=password_hashed)
        db.session.add(user_to_add)
        db.session.commit()

    app.cli.add_command(create_admin)
    return None
