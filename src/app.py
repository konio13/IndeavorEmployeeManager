from flask import Flask
from flask_cors import CORS
from src.config import Config
from src.database import init_db
from src.routes.employees import employees_bp
from src.routes.pages import pages_bp
from src.routes.skills import skills_bp
from src.routes.swagger import swagger_bp
from src.utils.error_handlers import init_error_handlers



def create_app():
    application = Flask(__name__)
    CORS(application)

    # configuration
    application.config.from_object(Config)

    # pages
    application.register_blueprint(pages_bp)

    # api
    application.register_blueprint(employees_bp)
    application.register_blueprint(skills_bp)

    # swagger api/docs
    application.register_blueprint(swagger_bp)

    # error handlers
    init_error_handlers(application)

    # database
    init_db(application)

    return application



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)