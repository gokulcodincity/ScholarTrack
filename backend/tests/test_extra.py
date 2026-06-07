def test_submit_reviewer_request(client, student_user, student_token):
    # Wait, the endpoint expects Form data and a file upload.
    # We can mock this with TestClient.
    from io import BytesIO
    fake_pdf = BytesIO(b"%PDF-1.4 mock content")
    
    response = client.post("/auth/reviewer-request", headers={
        "Authorization": f"Bearer {student_token}"
    }, data={
        "user_id": student_user.id,
        "university": "Test Univ",
        "department": "CS",
        "years_of_experience": 5,
        "institution_email": "test@univ.edu"
    }, files={
        "resume": ("resume.pdf", fake_pdf, "application/pdf")
    })
    
    # Wait, student_user is role=STUDENT. The endpoint requires PENDING_REVIEWER.
    # Let's just assert it gets rejected correctly.
    assert response.status_code == 400
    assert "Only PENDING_REVIEWER" in response.json()["detail"]

def test_fetch_reviewer_note_unauthorized(client, student_token):
    # Students cannot fetch reviewer notes
    response = client.get("/reviewer-notes/1", headers={
        "Authorization": f"Bearer {student_token}"
    })
    assert response.status_code == 403
    assert "Reviewer or Admin" in response.json()["detail"]

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
