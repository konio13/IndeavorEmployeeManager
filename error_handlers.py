from flask import jsonify


def init_error_handlers(app):
    """
    Register all error handlers with the Flask application
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Resource not found',
            'message': str(error)
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad request',
            'message': str(error)
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'Unauthorized',
            'message': str(error)
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 'Forbidden',
            'message': str(error)
        }), 403

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500

    # Handle generic exceptions
    @app.errorhandler(Exception)
    def handle_exception(error):
        # For unexpected errors, don't expose details in production
        return jsonify({
            'error': 'Internal server error',
            'message': 'Something went wrong'
        }), 500