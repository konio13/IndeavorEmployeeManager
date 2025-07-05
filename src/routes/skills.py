from flask import Blueprint, request, jsonify, abort

from src.database import db
from src.models.skill import Skill
from src.utils.decorators import require_api_key


skills_bp = Blueprint('skills', __name__, url_prefix='/api/skills')

@skills_bp.route('/', methods=['GET'])
@require_api_key
def get_skills():
    skills = Skill.query.all()
    return jsonify([skill.to_dict() for skill in skills])


@skills_bp.route('/<int:skill_id>', methods=['GET'])
@require_api_key
def get_skill(skill_id):
    skill = db.session.get(Skill, skill_id)
    return jsonify(skill.to_dict()) if skill else abort(404, description='Skill not found')


@skills_bp.route('/', methods=['POST'])
@require_api_key
def create_skill():
    data = request.get_json()

    if not data or 'name' not in data:
        abort(400, description='Missing required field: name')

    if Skill.query.filter_by(name=data['name']).first():
        abort(400, description='Skill with this name already exists')

    skill = Skill(
        name=data['name'],
        description=data.get('description', '')
    )

    db.session.add(skill)
    db.session.commit()

    return jsonify(skill.to_dict()), 201


@skills_bp.route('/<int:skill_id>', methods=['PUT'])
@require_api_key
def update_skill(skill_id):
    skill = db.session.get(Skill, skill_id)
    data = request.get_json()

    if not skill:
        abort(404, description='Skill not found')
    if not data:
        abort(400, description='No data provided')


    if 'name' in data:
        if Skill.query.filter_by(name=data['name']).filter(Skill.id != skill_id).first():
            abort(400, description='Skill with this name already exists')
        skill.name = data['name']

    if 'description' in data:
        skill.description = data['description']

    db.session.commit()
    return jsonify(skill.to_dict())


@skills_bp.route('/<int:skill_id>', methods=['DELETE'])
@require_api_key
def delete_skill(skill_id):
    skill = db.session.get(Skill, skill_id)

    if not skill:
        abort(404, description='Skill not found')

    db.session.delete(skill)
    db.session.commit()
    return jsonify({'message': 'Skill deleted successfully'})