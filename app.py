from flask import Flask, render_template
from flask_cors import CORS
from config import Config
from database import init_db
from error_handlers import init_error_handlers
from routes.employees import employees_bp
from routes.pages import pages_bp
from routes.skills import skills_bp

def create_app():
    application = Flask(__name__)
    CORS(application)

    application.config.from_object(Config)

    # pages
    application.register_blueprint(pages_bp)

    # api
    application.register_blueprint(employees_bp)
    application.register_blueprint(skills_bp)

    init_error_handlers(application)

    init_db(application)

    return application



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)