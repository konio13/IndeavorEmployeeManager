import re

from sqlalchemy.orm import validates

from src.database import db

employee_skills = db.Table('employee_skills',
                           db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'), primary_key=True),
                           db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
                           )


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    skills = db.relationship('Skill', secondary=employee_skills, backref='employees')

    @validates('name', 'surname')
    def validate_name_surname(self, key, value):
        if len(value) > 100:
            raise ValueError(f"{key} cannot exceed 100 characters")
        if not value or not value.strip():
            raise ValueError(f"{key} must not be empty or whitespace")
        return value

    @validates('email')
    def validate_email(self, key, value):
        email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not re.match(email_regex, value):
            raise ValueError("invalid email format")
        if len(value) > 120:
            raise ValueError("email cannot exceed 120 characters")
        return value


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'skills': [skill.to_dict() for skill in self.skills]
        }