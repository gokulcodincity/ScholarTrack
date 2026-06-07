def scholarship_payload(title="Student Count Scholarship"):
    return {
        "title": title,
        "field": "CS",
        "amount": 5000.00,
        "eligibility": "CGPA greater than 8.0",
        "deadline": "2026-12-31"
    }


def test_create_student_profile(client, admin_user, admin_token):
    # Setup user
    new_user_resp = client.post("/admin/users", headers={"Authorization": f"Bearer {admin_token}"}, json={
        "name": "New Student", "email": "newstudent@test.com", "password": "password123", "role": "STUDENT"
    })
    uid = new_user_resp.json()["id"]
    from app.config.security import create_access_token
    token = create_access_token({"id": uid, "role": "STUDENT"})

    # Create profile
    prof_resp = client.post("/students/", headers={"Authorization": f"Bearer {token}"}, json={
        "user_id": uid, "department": "Biology", "cgpa": 9.0, "academic_year": "2025"
    })
    assert prof_resp.status_code == 200
    assert prof_resp.json()["department"] == "Biology"

def test_student_profile_idor(client, student_user, student_token, admin_token):
    # Setup second student
    student2_resp = client.post("/admin/users", headers={"Authorization": f"Bearer {admin_token}"}, json={
        "name": "Student 2", "email": "student2x@test.com", "password": "password123", "role": "STUDENT"
    })
    s2_id = student2_resp.json()["id"]

    # Try to fetch S1 profile as S2
    from app.config.security import create_access_token
    s2_token = create_access_token({"id": s2_id, "role": "STUDENT"})

    fetch_resp = client.get(f"/students/{student_user.id}", headers={"Authorization": f"Bearer {s2_token}"})
    assert fetch_resp.status_code == 403
    assert "own profile" in fetch_resp.json()["error"]["message"].lower()

    # Admin should be able to view? Wait, the route says ONLY students can view. If so, skip. Let's just verify S1 can view own:
    fetch_own = client.get(f"/students/{student_user.id}", headers={"Authorization": f"Bearer {student_token}"})
    assert fetch_own.status_code == 200
    assert fetch_own.json()["cgpa"] == 8.5


def test_get_student_profile_includes_application_count(
    client,
    student_user,
    student_token,
    admin_token
):
    create_sch = client.post(
        "/scholarships/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=scholarship_payload()
    )
    sch_id = create_sch.json()["id"]

    client.post(
        "/applications/",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"student_id": student_user.id, "scholarship_id": sch_id}
    )

    response = client.get(
        f"/students/{student_user.id}",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    assert response.status_code == 200
    assert response.json()["application_count"] == 1
