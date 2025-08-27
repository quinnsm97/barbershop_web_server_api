from flask import jsonify

def register_error_handlers(app):
    """
    Registers custom error handlers for the Flask application.

    Parameters:
    app (Flask): The Flask application instance to which the error handlers will be registered.

    This function sets up handlers for HTTP status codes 400, 404, and 500, as well as a generic
    handler for all uncaught exceptions. Each handler returns a JSON response with an appropriate
    error message and HTTP status code.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"message": "Bad Request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"message": "Resource Not Found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"message": "Internal Server Error"}), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        return jsonify({"message": str(error)}), 500