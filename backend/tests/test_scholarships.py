def test_create_scholarship_as_admin(client, admin_token):
    response = client.post("/scholarships/", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json={
        "title": "Merit Scholarship",
        "field_of_study": "CS",
        "amount": 5000.00,
        "eligibility_criteria": "CGPA > 8.0",
        "deadline": "2026-12-31"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Merit Scholarship"

def test_create_scholarship_as_student(client, student_token):
    response = client.post("/scholarships/", headers={
        "Authorization": f"Bearer {student_token}"
    }, json={
        "title": "Hack Scholarship",
        "field_of_study": "CS",
        "amount": 5000.00,
        "eligibility_criteria": "CGPA > 8.0",
        "deadline": "2026-12-31"
    })
    assert response.status_code == 403

def test_get_scholarships(client, admin_token):
    # First create one
    client.post("/scholarships/", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json={
        "title": "Open Scholarship",
        "field_of_study": "Physics",
        "amount": 1000.00,
        "eligibility_criteria": "None",
        "deadline": "2026-12-31"
    })

    # Anyone can fetch
    response = client.get("/scholarships/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_update_scholarship(client, admin_token):
    # Create
    create_resp = client.post("/scholarships/", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json={
        "title": "Old Title",
        "field_of_study": "CS",
        "amount": 5000.00,
        "eligibility_criteria": "CGPA > 8.0",
        "deadline": "2026-12-31"
    })
    sch_id = create_resp.json()["id"]

    # Update
    response = client.put(f"/scholarships/{sch_id}", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json={
        "title": "New Title",
        "field_of_study": "CS",
        "amount": 6000.00,
        "eligibility_criteria": "CGPA > 8.5",
        "deadline": "2026-12-31"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["amount"] == 6000.00

def test_delete_scholarship(client, admin_token):
    create_resp = client.post("/scholarships/", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json={
        "title": "To Be Deleted",
        "field_of_study": "CS",
        "amount": 5000.00,
        "eligibility_criteria": "CGPA > 8.0",
        "deadline": "2026-12-31"
    })
    sch_id = create_resp.json()["id"]

    del_resp = client.delete(f"/scholarships/{sch_id}", headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert del_resp.status_code == 200

    # Verify deleted
    get_resp = client.get(f"/scholarships/{sch_id}")
    assert get_resp.status_code == 404