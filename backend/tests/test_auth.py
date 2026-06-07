def error_message(response):
    return response.json()["error"]["message"]


def test_register_duplicate_email(client, db):
    response = client.post("/auth/register", json={
        "name": "Alice",
        "email": "alice@test.com",
        "password": "password123",
        "role": "STUDENT"
    })
    assert response.status_code == 200

    response = client.post("/auth/register", json={
        "name": "Alice2",
        "email": "alice@test.com",
        "password": "password123",
        "role": "STUDENT"
    })
    assert response.status_code == 400
    assert "Email already exists" in error_message(response)


def test_register_success_creates_student_profile(client):
    response = client.post("/auth/register", json={
        "name": "Dana",
        "email": "dana@test.com",
        "password": "password123",
        "role": "STUDENT",
        "department": "Math",
        "cgpa": 8.7,
        "academic_year": "2025"
    })

    assert response.status_code == 200
    assert response.json()["role"] == "STUDENT"

    from app.models.student import Student
    from app.config.database import SessionLocal

    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.department == "Math").first()
        assert student is not None
        assert student.cgpa == 8.7
    finally:
        db.close()

def test_register_privilege_escalation(client):
    response = client.post("/auth/register", json={
        "name": "Attacker",
        "email": "hacker@test.com",
        "password": "password123",
        "role": "ADMIN"
    })
    assert response.status_code == 403
    assert "restricted" in error_message(response).lower()

def test_login_unverified_email(client, db):
    # Register but don't verify
    client.post("/auth/register", json={
        "name": "Bob",
        "email": "bob@test.com",
        "password": "password123",
        "role": "STUDENT"
    })
    
    response = client.post("/auth/login", json={
        "email": "bob@test.com",
        "password": "password123"
    })
    assert response.status_code == 403
    assert "verify your email" in error_message(response)

def test_login_wrong_password(client, student_user):
    response = client.post("/auth/login", json={
        "email": student_user.email,
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert error_message(response) == "Invalid credentials"


def test_login_success_for_verified_user(client, student_user):
    response = client.post("/auth/login", json={
        "email": student_user.email,
        "password": "password123"
    })

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]

def test_create_admin_user_as_admin(client, admin_token):
    response = client.post("/admin/users", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json={
        "name": "New Admin",
        "email": "newadmin@test.com",
        "password": "password123",
        "role": "ADMIN"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "newadmin@test.com"

def test_create_admin_user_as_student(client, student_token):
    response = client.post("/admin/users", headers={
        "Authorization": f"Bearer {student_token}"
    }, json={
        "name": "New Admin",
        "email": "newadmin@test.com",
        "password": "password123",
        "role": "ADMIN"
    })
    assert response.status_code == 403
