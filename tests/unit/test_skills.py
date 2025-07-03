from src.config import Config
from src.database import db
from src.models.skill import Skill


HEADERS = {"x-api-key": Config.API_AUTHENTICATION_KEY}


def test_get_skills_empty(client):
    response = client.get("/api/skills/", headers=HEADERS)
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_skill(client):
    data = {"name": "Python", "description": "Programming language"}
    response = client.post("/api/skills/", json=data, headers=HEADERS)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["name"] == "Python"
    assert json_data["description"] == "Programming language"

def test_create_skill_missing_name(client):
    response = client.post("/api/skills/", json={}, headers=HEADERS)
    assert response.status_code == 400
    assert "error" in response.get_json()
    assert "Missing required field: name" in response.get_json()["error"]

def test_create_skill_missing_description(client):
    data = {"name": "Java"}
    response = client.post("/api/skills/", json=data, headers=HEADERS)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["name"] == data["name"]
    assert json_data["description"] == ""

def test_get_skill_by_id(client):
    skill = Skill(name="Django", description="Web framework")
    db.session.add(skill)
    db.session.commit()
    response = client.get(f"/api/skills/{skill.id}", headers=HEADERS)
    assert response.status_code == 200
    assert response.get_json()["name"] == skill.name
    assert response.get_json()["description"] == skill.description

def test_get_skill_by_id_unknown(client):
    response = client.get(f"/api/skills/1", headers=HEADERS)
    assert response.status_code == 404

def test_update_skill(client):
    skill = Skill(name="Flask-Old", description="Old desc")
    db.session.add(skill)
    db.session.commit()
    data = {"name": "Flask-New", "description": "New desc"}
    response = client.put(f"/api/skills/{skill.id}", json=data, headers=HEADERS)
    assert response.status_code == 200
    assert response.get_json()["name"] == data["name"]
    assert response.get_json()["description"] == data["description"]

def test_delete_skill(client):
    skill = Skill(name="DeleteMe", description="")
    db.session.add(skill)
    db.session.commit()
    response = client.delete(f"/api/skills/{skill.id}", headers=HEADERS)
    assert response.status_code == 200
    assert response.get_json()["message"] == "Skill deleted successfully"
