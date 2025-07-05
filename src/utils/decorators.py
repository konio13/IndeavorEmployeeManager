from functools import wraps
from flask import request, jsonify, abort
from src.config import Config


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != Config.API_AUTHENTICATION_KEY:
            abort(401, description='Unauthorized access')
        return f(*args, **kwargs)
    return decorated