import os

from flask import Flask

from controllers.cli_controller import db_commands
from controllers.customer_controller import customer_bp
from controllers.staff_controller import staff_bp
from controllers.appointment_controller import appointment_bp
from init import db


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    db.init_app(app)

    app.json.sort_keys = False

    app.register_blueprint(db_commands)
    app.register_blueprint(customer_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(appointment_bp)

    return app
