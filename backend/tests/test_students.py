def test_create_student_profile(client, admin_user, admin_token):
    # Setup user
    new_user_resp = client.post("/admin/users", headers={"Authorization": f"Bearer {admin_token}"}, json={
        "name": "New Student", "email": "newstudent@test.com", "password": "pass", "role": "STUDENT"
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
        "name": "Student 2", "email": "student2x@test.com", "password": "pass", "role": "STUDENT"
    })
    s2_id = student2_resp.json()["id"]

    # Try to fetch S1 profile as S2
    from app.config.security import create_access_token
    s2_token = create_access_token({"id": s2_id, "role": "STUDENT"})

    fetch_resp = client.get(f"/students/{student_user.id}", headers={"Authorization": f"Bearer {s2_token}"})
    assert fetch_resp.status_code == 403
    assert "own profile" in fetch_resp.json()["detail"].lower()

    # Admin should be able to view? Wait, the route says ONLY students can view. If so, skip. Let's just verify S1 can view own:
    fetch_own = client.get(f"/students/{student_user.id}", headers={"Authorization": f"Bearer {student_token}"})
    assert fetch_own.status_code == 200
    assert fetch_own.json()["cgpa"] == 8.5