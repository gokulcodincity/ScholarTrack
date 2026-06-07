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
    assert "Email already exists" in response.json()["detail"]

def test_register_privilege_escalation(client):
    response = client.post("/auth/register", json={
        "name": "Attacker",
        "email": "hacker@test.com",
        "password": "password123",
        "role": "ADMIN"
    })
    assert response.status_code == 403
    assert "restricted" in response.json()["detail"].lower()

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
    assert response.status_code == 400
    assert response.json()["detail"] == "Email not verified"

def test_login_wrong_password(client, student_user):
    response = client.post("/auth/login", json={
        "email": student_user.email,
        "password": "wrongpassword"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid credentials"

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