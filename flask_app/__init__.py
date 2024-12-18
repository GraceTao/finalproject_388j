# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime
import os
from dotenv import load_dotenv

# local
from .client import OnetWebService

load_dotenv()

db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
careers_client = OnetWebService(os.environ.get("ONET_USERNAME"), os.environ.get("ONET_PASSWORD"))

from .users.routes import users
from .careers.routes import careers


def custom_404(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    #app.config["MONGODB_HOST"] = os.environ.get("MONGODB_HOST")
    app.config["MONGO_URI"] = "mongodb://localhost:27017/my_database"

    # app.config.from_pyfile("config.py", silent=False)
    # if test_config is not None:
    #     app.config.update(test_config)


    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(careers)
    app.register_error_handler(404, custom_404)

    login_manager.login_view = "users.login"

    with app.app_context():
        try:
            db.connection
            print("Database connected successfully!")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    return app
