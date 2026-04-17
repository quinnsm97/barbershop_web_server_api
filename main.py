import os

from flask import Flask
from dotenv import load_dotenv

from utils.error_handler import register_error_handlers
from controllers.cli_controller import db_commands
from controllers.customer_controller import customer_bp
from controllers.staff_controller import staff_bp
from controllers.appointment_controller import appointment_bp
from controllers.service_controller import service_bp
from init import db

load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")

    # Health check route
    @app.route("/")
    def health():
        return {"status": "ok"}

    db.init_app(app)

    with app.app_context():
        try:
            db.create_all()
            print("✅ Tables created")
        except Exception as e:
            print("❌ DB init failed:", e)

    app.json.sort_keys = False

    app.register_blueprint(db_commands)
    app.register_blueprint(customer_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(service_bp)

    register_error_handlers(app)

    return app
