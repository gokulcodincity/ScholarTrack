def scholarship_payload(
    title="Merit Scholarship",
    field="CS",
    amount=5000.00,
    eligibility="CGPA greater than 8.0",
    deadline="2026-12-31"
):
    return {
        "title": title,
        "field": field,
        "amount": amount,
        "eligibility": eligibility,
        "deadline": deadline
    }


def test_create_scholarship_as_admin(client, admin_token):
    response = client.post("/scholarships/", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json=scholarship_payload())
    assert response.status_code == 200
    assert response.json()["title"] == "Merit Scholarship"

def test_create_scholarship_as_student(client, student_token):
    response = client.post("/scholarships/", headers={
        "Authorization": f"Bearer {student_token}"
    }, json=scholarship_payload(title="Hack Scholarship"))
    assert response.status_code == 403

def test_get_scholarships(client, admin_token, student_token):
    # First create one
    client.post("/scholarships/", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json=scholarship_payload(
        title="Open Scholarship",
        field="Physics",
        amount=1000.00,
        eligibility="Open to all qualified students"
    ))

    response = client.get(
        "/scholarships/",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_update_scholarship(client, admin_token):
    # Create
    create_resp = client.post("/scholarships/", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json=scholarship_payload(title="Old Title"))
    sch_id = create_resp.json()["id"]

    # Update
    response = client.patch(f"/scholarships/{sch_id}", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json={
        "title": "New Title",
        "field": "CS",
        "amount": 6000.00,
        "eligibility": "CGPA greater than 8.5",
        "deadline": "2026-12-31"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["amount"] == 6000.00

def test_delete_scholarship(client, admin_token):
    create_resp = client.post("/scholarships/", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json=scholarship_payload(title="To Be Deleted"))
    sch_id = create_resp.json()["id"]

    del_resp = client.delete(f"/scholarships/{sch_id}", headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert del_resp.status_code == 200

    # Verify deleted
    get_resp = client.get(
        f"/scholarships/{sch_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert get_resp.status_code == 404


def test_filter_scholarships_by_field_and_min_amount(
    client,
    admin_token,
    student_token
):
    client.post(
        "/scholarships/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=scholarship_payload(
            title="Physics Grant",
            field="Physics",
            amount=2000.00,
            eligibility="Physics students with strong records"
        )
    )
    client.post(
        "/scholarships/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=scholarship_payload(
            title="CS Excellence",
            field="Computer Science",
            amount=9000.00,
            eligibility="Computer science students with strong records"
        )
    )

    response = client.get(
        "/scholarships/?field=Computer&min_amount=5000",
        headers={"Authorization": f"Bearer {student_token}"}
    )

    assert response.status_code == 200
    titles = [scholarship["title"] for scholarship in response.json()]
    assert titles == ["CS Excellence"]


def test_scholarship_stats_counts_applications(
    client,
    admin_token,
    student_user,
    student_token
):
    create_resp = client.post(
        "/scholarships/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=scholarship_payload(title="Stats Scholarship")
    )
    sch_id = create_resp.json()["id"]
    client.post(
        "/applications/",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"student_id": student_user.id, "scholarship_id": sch_id}
    )

    response = client.get(
        f"/scholarships/{sch_id}/stats",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200
    assert response.json()["total_applied"] == 1
    assert response.json()["awarded"] == 0
