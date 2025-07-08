# Indeavor - EmployeeManagement Demo

**EmployeeManagement** is a custom-made Python Flask application demonstrating employee and skill management using SQLAlchemy ORM with extensible architecture.

---

## 🏗️ Features

- Modular Flask blueprint structure
- SQLAlchemy ORM (file-based SQLite DB by default)
- API Key protected endpoints
- Model-level validations (length, format, required fields)
- Swagger UI for interactive API docs

---

## 🚀 Getting Started

### 1. Clone the Project

```
git clone https://github.com/konio13/IndeavorEmployeeManager
````

### 2. Create & Activate Virtual Environment

```
python -m venv .venv

.venv\Scripts\activate  # For Windows
# OR
source .venv/bin/activate    # On macOS/Linux
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Run the Application

```
python -m src.app
```

The app will start at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📦 Database

* Uses SQLite (`employees.db`) by default
* Auto-generated on first run via `db.create_all()`
* Easily switch to PostgreSQL or other DBs by updating `SQLALCHEMY_DATABASE_URI`

---

## ✅ API Validation

* Model fields (e.g., `name`, `surname`, `email`) are validated for:

  * Max length (100)
  * No whitespace-only input
  * Email format (regex)
* API errors return JSON responses with custom messages, e.g.:

  ```json
  {
    "error": "Bad request",
    "message": "Email format is not valid"
  }
  ```

---

## 🧪 Swagger API Docs

Access all documented endpoints via:

**[Swagger UI → http://127.0.0.1:5000/api/docs/#/](http://127.0.0.1:5000/api/docs/#/)**

---

## 🧰 Useful Commands

| Task                   | Command                          |
| ---------------------- | -------------------------------- |
| Activate venv          | `.venv\Scripts\activate`         |
| Run Flask app          | `python -m src.app`              |
| Deactivate venv        | `deactivate`                     |


---

## 📂 Project Structure (Simplified)

```
.
├── src/
│   ├── app.py
│   ├── routes/    (endpoints)
│   ├── models/    (db models)
│   ├── templates/ (UI: html files)
│   └── utils/     (error handlers)
├── tests/
│   └── unit/
├── requirements.txt
└── README.md
```

---

## 📝 Notes

* Designed for easy backend replacement (e.g., real SQL, MongoDB)
* `swagger.json` defines schemas like POST body requirements
* Full error handling with `@app.errorhandler` for 400s, 404s, etc.

---

## 🔒 Security

* All endpoints protected with `@require_api_key`
* Uses HTTP headers for authentication

---

### 🧪 Running Unit Tests

This project uses **[pytest](https://docs.pytest.org/)** for unit testing.

#### ✅ To run all tests:

```
pytest
```


#### 🔍 Example command to run tests with detailed output:

```
pytest -v
```

#### 🧪 Run a specific test file:

```
pytest tests/test_employees.py
```

---
