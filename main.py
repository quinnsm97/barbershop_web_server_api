from flask import Flask
from controllers.cli_controller import db_commands
from controllers.customer_controller import customer_bp

from init import db
import os

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    db.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(customer_bp)

    return app
