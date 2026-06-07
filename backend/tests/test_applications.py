def scholarship_payload(title="App Test Scholarship"):
    return {
        "title": title,
        "field": "CS",
        "amount": 5000.00,
        "eligibility": "CGPA greater than 8.0",
        "deadline": "2026-12-31"
    }


def create_application(client, student_user, student_token, admin_token, title):
    create_sch = client.post(
        "/scholarships/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=scholarship_payload(title=title)
    )
    sch_id = create_sch.json()["id"]
    app_resp = client.post(
        "/applications/",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"student_id": student_user.id, "scholarship_id": sch_id}
    )
    return app_resp.json(), sch_id


def test_create_application_as_student(client, student_user, student_token, admin_token):
    # First create a scholarship
    create_sch = client.post("/scholarships/", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json=scholarship_payload())
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
    assert "already exists" in response2.json()["error"]["message"].lower()

def test_application_idor_protection(client, student_user, student_token, admin_token, reviewer_token):
    # Create scholarship
    create_sch = client.post("/scholarships/", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json=scholarship_payload(title="IDOR Scholarship"))
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
        "name": "Student 2", "email": "student2@test.com", "password": "password123", "role": "STUDENT"
    })
    from app.config.security import create_access_token
    student2_token = create_access_token({"id": student2_resp.json()["id"], "role": "STUDENT"})

    # Student 2 tries to fetch Student 1's application
    fetch_resp = client.get(f"/applications/{app_id}", headers={"Authorization": f"Bearer {student2_token}"})
    assert fetch_resp.status_code == 403
    assert "only view your own" in fetch_resp.json()["error"]["message"].lower()

    # Unassigned reviewer tries to fetch
    fetch_reviewer = client.get(f"/applications/{app_id}", headers={"Authorization": f"Bearer {reviewer_token}"})
    assert fetch_reviewer.status_code == 403
    assert "not assigned" in fetch_reviewer.json()["error"]["message"].lower()

def test_assign_reviewer_as_admin(client, student_user, student_token, admin_token, reviewer_user):
    # Setup Scholarship and Application
    create_sch = client.post("/scholarships/", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json=scholarship_payload(title="Assign Scholarship"))
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


def test_student_applications_lists_only_student_records(
    client,
    student_user,
    student_token,
    admin_token
):
    application, _ = create_application(
        client,
        student_user,
        student_token,
        admin_token,
        "Student List Scholarship"
    )

    response = client.get(
        f"/applications/?student_id={student_user.id}",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [application["id"]]


def test_reviewer_applications_lists_assigned_records(
    client,
    student_user,
    student_token,
    admin_token,
    reviewer_user,
    reviewer_token
):
    application, _ = create_application(
        client,
        student_user,
        student_token,
        admin_token,
        "Reviewer List Scholarship"
    )
    client.patch(
        f"/applications/{application['id']}/assign",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"reviewer_id": reviewer_user.id}
    )

    response = client.get(
        f"/applications/?reviewer_id={reviewer_user.id}",
        headers={"Authorization": f"Bearer {reviewer_token}"}
    )

    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [application["id"]]


def test_application_detail_merges_essay_review_and_decision_status(
    client,
    clean_mongodb,
    student_user,
    student_token,
    admin_token,
    reviewer_user,
    reviewer_token
):
    application, _ = create_application(
        client,
        student_user,
        student_token,
        admin_token,
        "Detail Merge Scholarship"
    )
    app_id = application["id"]
    client.post(
        "/essays/",
        headers={"Authorization": f"Bearer {student_token}"},
        json={
            "application_id": app_id,
            "essay": "My detailed essay",
            "supporting_content": "portfolio"
        }
    )
    client.patch(
        f"/applications/{app_id}/assign",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"reviewer_id": reviewer_user.id}
    )
    client.post(
        "/reviewer-notes/",
        headers={"Authorization": f"Bearer {reviewer_token}"},
        json={
            "application_id": app_id,
            "reviewer_notes": "Strong candidate",
            "score": 91,
            "scoring_rationale": "Strong essay"
        }
    )

    response = client.get(
        f"/applications/{app_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["application"]["id"] == app_id
    assert body["essay"]["essay"] == "My detailed essay"
    assert body["reviewer_note"]["score"] == 91
    assert body["decision_recorded"] is False
