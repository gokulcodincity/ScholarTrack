def test_create_application_as_student(client, student_user, student_token, admin_token):
    # First create a scholarship
    create_sch = client.post("/scholarships/", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json={
        "title": "App Test Scholarship",
        "field_of_study": "CS",
        "amount": 5000.00,
        "eligibility_criteria": "CGPA > 8.0",
        "deadline": "2026-12-31"
    })
    sch_id = create_sch.json()["id"]

    # Apply as student
    response = client.post("/applications/", headers={
        "Authorization": f"Bearer {student_token}"
    }, json={
        "student_id": student_user.id,
        "scholarship_id": sch_id
    })
    assert response.status_code == 200
    assert response.json()["status"] == "PENDING"

    # Cannot apply twice
    response2 = client.post("/applications/", headers={
        "Authorization": f"Bearer {student_token}"
    }, json={
        "student_id": student_user.id,
        "scholarship_id": sch_id
    })
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"].lower()

def test_application_idor_protection(client, student_user, student_token, admin_token, reviewer_token):
    # Create scholarship
    create_sch = client.post("/scholarships/", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json={
        "title": "IDOR Scholarship",
        "field_of_study": "CS",
        "amount": 5000.00,
        "eligibility_criteria": "CGPA > 8.0",
        "deadline": "2026-12-31"
    })
    sch_id = create_sch.json()["id"]

    # Student 1 applies
    app_resp = client.post("/applications/", headers={
        "Authorization": f"Bearer {student_token}"
    }, json={
        "student_id": student_user.id,
        "scholarship_id": sch_id
    })
    app_id = app_resp.json()["id"]

    # Admin creates Student 2
    student2_resp = client.post("/admin/users", headers={"Authorization": f"Bearer {admin_token}"}, json={
        "name": "Student 2", "email": "student2@test.com", "password": "pass", "role": "STUDENT"
    })
    from app.config.security import create_access_token
    student2_token = create_access_token({"id": student2_resp.json()["id"], "role": "STUDENT"})

    # Student 2 tries to fetch Student 1's application
    fetch_resp = client.get(f"/applications/{app_id}", headers={"Authorization": f"Bearer {student2_token}"})
    assert fetch_resp.status_code == 403
    assert "only view your own" in fetch_resp.json()["detail"].lower()

    # Unassigned reviewer tries to fetch
    fetch_reviewer = client.get(f"/applications/{app_id}", headers={"Authorization": f"Bearer {reviewer_token}"})
    assert fetch_reviewer.status_code == 403
    assert "not assigned" in fetch_reviewer.json()["detail"].lower()

def test_assign_reviewer_as_admin(client, student_user, student_token, admin_token, reviewer_user):
    # Setup Scholarship and Application
    create_sch = client.post("/scholarships/", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json={
        "title": "Assign Scholarship",
        "field_of_study": "CS",
        "amount": 5000.00,
        "eligibility_criteria": "CGPA > 8.0",
        "deadline": "2026-12-31"
    })
    sch_id = create_sch.json()["id"]

    app_resp = client.post("/applications/", headers={
        "Authorization": f"Bearer {student_token}"
    }, json={"student_id": student_user.id, "scholarship_id": sch_id})
    app_id = app_resp.json()["id"]

    # Admin assigns reviewer
    assign_resp = client.patch(f"/applications/{app_id}/assign", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json={"reviewer_id": reviewer_user.id})
    
    assert assign_resp.status_code == 200
    assert assign_resp.json()["status"] == "UNDER_REVIEW"