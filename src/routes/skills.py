from flask import Blueprint, request, jsonify

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
    skill = Skill.query.get_or_404(skill_id)
    return jsonify(skill.to_dict())


@skills_bp.route('/', methods=['POST'])
@require_api_key
def create_skill():
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({'error': 'Missing required field: name'}), 400

    if Skill.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Skill with this name already exists'}), 400

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
    skill = Skill.query.get_or_404(skill_id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'name' in data:
        if Skill.query.filter_by(name=data['name']).filter(Skill.id != skill_id).first():
            return jsonify({'error': 'Skill with this name already exists'}), 400
        skill.name = data['name']

    if 'description' in data:
        skill.description = data['description']

    db.session.commit()
    return jsonify(skill.to_dict())


@skills_bp.route('/<int:skill_id>', methods=['DELETE'])
@require_api_key
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    return jsonify({'message': 'Skill deleted successfully'})