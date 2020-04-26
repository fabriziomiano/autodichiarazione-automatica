import os

from flask import Flask
from flask_wtf import CSRFProtect

from .views.frontend import frontend


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.urandom(32)
    app.register_blueprint(frontend)
    CSRFProtect(app)
    return app
