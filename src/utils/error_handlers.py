
from flask import jsonify
from werkzeug.exceptions import HTTPException


def init_error_handlers(app):
    """
    Register all error handlers with the Flask application
    """

    def get_error_msg(error):
        return error.description if isinstance(error, HTTPException) else str(error)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Resource not found',
            'message': get_error_msg(error)
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad request',
            'message': get_error_msg(error)
        }), 400



    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'Unauthorized',
            'message': get_error_msg(error)
        }), 401

    @app.errorhandler(403)
    @app.errorhandler(ValueError)
    def forbidden(error):
        return jsonify({
            'error': 'Forbidden',
            'message': get_error_msg(error)
        }), 403

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred' + get_error_msg(error)
        }), 500

    # Handle generic exceptions
    @app.errorhandler(Exception)
    def handle_exception(error):
        return jsonify({
            'error': 'Internal server error',
            'message': 'Something went wrong' + get_error_msg(error)
        }), 500