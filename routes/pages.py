from flask import Blueprint, render_template


pages_bp = Blueprint('pages', __name__, url_prefix='/pages')


# Route to serve the HTML file ---
@pages_bp.route('/dashboard', methods=['GET'])
def index():
    return render_template('index.html')


@pages_bp.route('/update_employee', methods=['GET'])
def update_employee():
    return render_template('update_employee.html')


@pages_bp.route('/update_skill', methods=['GET'])
def update_skill():
    return render_template('update_skill.html')