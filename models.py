from database import db

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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'skills': [skill.to_dict() for skill in self.skills]
        }


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }