def test_full_decision_lifecycle(client, student_user, student_token, admin_token, reviewer_user, reviewer_token):
    # 1. Admin creates scholarship
    create_sch = client.post("/scholarships/", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json={
        "title": "End-to-End Scholarship",
        "field_of_study": "CS",
        "amount": 5000.00,
        "eligibility_criteria": "CGPA > 8.0",
        "deadline": "2026-12-31"
    })
    sch_id = create_sch.json()["id"]

    # 2. Student applies
    app_resp = client.post("/applications/", headers={
        "Authorization": f"Bearer {student_token}"
    }, json={"student_id": student_user.id, "scholarship_id": sch_id})
    app_id = app_resp.json()["id"]

    # 3. Student submits essay
    client.post("/essays/", headers={"Authorization": f"Bearer {student_token}"}, json={
        "application_id": app_id,
        "essay": "My amazing essay",
        "supporting_content": "github.com/myprofile"
    })

    # 4. Admin assigns reviewer
    client.patch(f"/applications/{app_id}/assign", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json={"reviewer_id": reviewer_user.id})

    # 5. Reviewer submits review note and score
    client.post("/reviewer-notes/", headers={"Authorization": f"Bearer {reviewer_token}"}, json={
        "application_id": app_id,
        "reviewer_notes": "Great candidate!",
        "score": 95.5,
        "scoring_rationale": "High GPA and good projects"
    })

    # 6. Reviewer completes review
    rev_comp_resp = client.patch(f"/applications/{app_id}/review", headers={
        "Authorization": f"Bearer {reviewer_token}"
    })
    assert rev_comp_resp.status_code == 200
    assert rev_comp_resp.json()["review_completed"] == True

    # 7. Admin records final decision
    dec_resp = client.post("/admin/decisions", headers={
        "Authorization": f"Bearer {admin_token}"
    }, json={
        "application_id": app_id,
        "decision_status": "AWARDED"
    })
    
    assert dec_resp.status_code == 200
    assert dec_resp.json()["decision_status"] == "AWARDED"

def test_decision_only_after_review(client, student_user, student_token, admin_token, reviewer_user):
    # Setup
    create_sch = client.post("/scholarships/", headers={"Authorization": f"Bearer {admin_token}"}, json={
        "title": "Fail Decision Scholarship", "field_of_study": "CS", "amount": 5000.00, "eligibility_criteria": "None", "deadline": "2026-12-31"
    })
    sch_id = create_sch.json()["id"]
    app_resp = client.post("/applications/", headers={"Authorization": f"Bearer {student_token}"}, json={"student_id": student_user.id, "scholarship_id": sch_id})
    app_id = app_resp.json()["id"]

    # Try decision without review
    dec_resp = client.post("/admin/decisions", headers={"Authorization": f"Bearer {admin_token}"}, json={
        "application_id": app_id, "decision_status": "AWARDED"
    })
    assert dec_resp.status_code == 400
    assert "Review may not be completed" in dec_resp.json()["detail"]