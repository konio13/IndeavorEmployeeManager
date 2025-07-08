from src.config import Config
from src.database import db
from src.models.employee import Employee
from src.models.skill import Skill

HEADERS = {"x-api-key": Config.API_AUTHENTICATION_KEY}

def test_get_employees_empty(client):
    response = client.get("/api/employees/", headers=HEADERS)
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_employee(client):
    data = {
        "name": "Nick",
        "surname": "Doe",
        "email": "nick.doe@example.com",
        "skill_ids": []
    }
    response = client.post("/api/employees/", json=data, headers=HEADERS)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["name"] == data["name"]
    assert json_data["surname"] == data["surname"]
    assert json_data["email"] == data["email"]
    assert json_data["skills"] == []

def test_create_employee_missing_name(client):
    data = {
        "surname": "Doe",
        "email": "nick.doe@example.com",
        "skill_ids": []
    }
    response = client.post("/api/employees/", json=data, headers=HEADERS)
    assert response.status_code == 400
    assert "error" in response.get_json()
    assert "Missing required fields: name, surname, email" in response.get_json()["message"]

def test_create_employee_missing_surname(client):
    data = {
        "name": "Nick",
        "email": "nick.doe@example.com",
        "skill_ids": []
    }
    response = client.post("/api/employees/", json=data, headers=HEADERS)
    assert response.status_code == 400
    assert "error" in response.get_json()
    assert "Missing required fields: name, surname, email" in response.get_json()["message"]

def test_create_employee_missing_email(client):
    data = {
        "name": "Nick",
        "surname": "Doe",
        "skill_ids": []
    }
    response = client.post("/api/employees/", json=data, headers=HEADERS)
    assert response.status_code == 400
    assert "error" in response.get_json()
    assert "Missing required fields: name, surname, email" in response.get_json()["message"]

def test_create_employee_missing_skills(client):
    data = {
        "name": "Nick",
        "surname": "Doe",
        "email": "nick.doe@example.com"
    }
    response = client.post("/api/employees/", json=data, headers=HEADERS)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["name"] == data["name"]
    assert json_data["surname"] == data["surname"]
    assert json_data["email"] == data["email"]
    assert json_data["skills"] == []

def test_get_employee_by_id(client):
    skill = Skill(name="Django", description="Web framework")
    db.session.add(skill)
    db.session.commit()
    employee = Employee(name="David", surname="Turu", email="david.turu@gmail.com", skills=[skill])
    db.session.add(employee)
    db.session.commit()
    response = client.get(f"/api/employees/{employee.id}", headers=HEADERS)
    assert response.status_code == 200
    assert response.get_json()["id"] == employee.id
    assert response.get_json()["name"] == employee.name
    assert response.get_json()["surname"] == employee.surname
    assert response.get_json()["email"] == employee.email
    assert response.get_json()["skills"] == [skill.to_dict()]

def test_get_employee_by_id_unknown(client):
    response = client.get(f"/api/employees/1", headers=HEADERS)
    assert response.status_code == 404

def test_update_employee(client):
    skill_old = Skill(name="Django", description="Web framework")
    skill_new = Skill(name="Spring", description="Java framework")
    db.session.add(skill_old)
    db.session.add(skill_new)
    db.session.commit()
    employee = Employee(name="David", surname="Turu", email="david.turu@gmail.com", skills=[skill_old])
    db.session.add(employee)
    db.session.commit()
    updated_employee_info = {
        'name': 'Sam',
        'surname': 'Villager',
        'email': 'sam.villager@gmail.com',
        'skill_ids': [skill_new.id]
    }
    response = client.put(f"/api/employees/{employee.id}", json=updated_employee_info, headers=HEADERS)
    assert response.status_code == 200
    assert response.get_json()["id"] == employee.id
    assert response.get_json()["name"] == updated_employee_info["name"]
    assert response.get_json()["surname"] == updated_employee_info["surname"]
    assert response.get_json()["email"] == updated_employee_info["email"]
    assert response.get_json()["skills"] == [skill_new.to_dict()]

def test_delete_employee(client):
    employee = Employee(name="David", surname="Turu", email="david.turu@gmail.com")
    db.session.add(employee)
    db.session.commit()
    response = client.delete(f"/api/employees/{employee.id}", headers=HEADERS)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Employee deleted successfully"

def test_search_employee_by_name(client):
    skill = Skill(name="Django", description="Web framework")
    db.session.add(skill)
    db.session.commit()
    employee = Employee(name="David", surname="Turu", email="david.turu@gmail.com", skills=[skill])
    db.session.add(employee)
    db.session.commit()
    response = client.get("/api/employees/search", query_string={'name': 'David'}, headers=HEADERS)
    assert response.status_code == 200
    assert any(emp["id"] == employee.id for emp in response.get_json())

def test_search_employee_by_skill_name(client):
    skill = Skill(name="Django", description="Web framework")
    db.session.add(skill)
    db.session.commit()
    employee_one = Employee(name="David", surname="Turu", email="david.turu@gmail.com", skills=[skill])
    employee_two = Employee(name="Sam", surname="West", email="sam.west@gmail.com", skills=[skill])
    db.session.add(employee_one)
    db.session.add(employee_two)
    db.session.commit()
    response = client.get("/api/employees/search", query_string={'skill': skill.name }, headers=HEADERS)
    assert response.status_code == 200
    assert any(emp["id"] == employee_one.id for emp in response.get_json())
    assert any(emp["id"] == employee_two.id for emp in response.get_json())