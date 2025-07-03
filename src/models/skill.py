from sqlalchemy.orm import validates

from src.database import db


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    @validates('name')
    def validate_name(self, key, value):
        if len(value) > 100:
            raise ValueError("Name cannot exceed 100 characters")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

