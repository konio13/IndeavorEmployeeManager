from flask import Blueprint, request, jsonify
from src.models.employee import Employee
from src.models.skill import Skill
from src.database import db
from src.utils.decorators import require_api_key


employees_bp = Blueprint('employees', __name__, url_prefix='/api/employees')


@employees_bp.route('/', methods=['GET'])
@require_api_key
def get_employees():
    employees = Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees])


@employees_bp.route('/<int:emp_id>', methods=['GET'])
@require_api_key
def get_employee(emp_id):
    employee = db.session.get(Employee, emp_id)
    return jsonify(employee.to_dict()) if employee else (jsonify({'error': 'Employee not found'}), 404)


@employees_bp.route('/', methods=['POST'])
@require_api_key
def create_employee():
    data = request.get_json()

    if not data or not all(k in data for k in ('name', 'surname', 'email')):
        return jsonify({'error': 'Missing required fields: name, surname, email'}), 400

    if Employee.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Employee with this email already exists'}), 400

    employee = Employee(
        name=data['name'],
        surname=data['surname'],
        email=data['email']
    )

    # Add skills if provided
    if 'skill_ids' in data:
        skills = Skill.query.filter(Skill.id.in_(data['skill_ids'])).all()
        employee.skills = skills

    db.session.add(employee)
    db.session.commit()

    return jsonify(employee.to_dict()), 201


@employees_bp.route('/<int:emp_id>', methods=['PUT'])
@require_api_key
def update_employee(emp_id):
    employee = db.session.get(Employee, emp_id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'name' in data:
        employee.name = data['name']
    if 'surname' in data:
        employee.surname = data['surname']
    if 'email' in data:
        if Employee.query.filter_by(email=data['email']).filter(Employee.id != emp_id).first():
            return jsonify({'error': 'Employee with this email already exists'}), 400
        employee.email = data['email']

    if 'skill_ids' in data:
        skills = Skill.query.filter(Skill.id.in_(data['skill_ids'])).all()
        employee.skills = skills

    db.session.commit()
    return jsonify(employee.to_dict())


@employees_bp.route('/<int:emp_id>', methods=['DELETE'])
@require_api_key
def delete_employee(emp_id):
    employee = db.session.get(Employee, emp_id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted successfully'})


@employees_bp.route('/search', methods=['GET'])
@require_api_key
def search_employees():
    name = request.args.get('name')
    surname = request.args.get('surname')
    skill = request.args.get('skill')

    query = Employee.query

    if name:
        query = query.filter(Employee.name.ilike(f'%{name}%'))
    if surname:
        query = query.filter(Employee.surname.ilike(f'%{surname}%'))
    if skill:
        query = query.join(Employee.skills).filter(Skill.name.ilike(f'%{skill}%'))

    employees = query.all()
    return jsonify([emp.to_dict() for emp in employees])