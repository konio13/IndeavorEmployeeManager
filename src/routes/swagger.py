from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL = '/api/docs'
SWAGGER_SPEC_JSON = '/static/swagger.json'  # Path to your Swagger spec

swagger_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    SWAGGER_SPEC_JSON
)



