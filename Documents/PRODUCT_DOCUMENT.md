# ScholarTrack Product Document

## 1. What The Application Does

ScholarTrack helps manage the scholarship process from discovery to final decision. Students can register, verify their email, browse scholarships, submit applications, and provide essays. Reviewers can review assigned applications and submit scores. Admins can manage scholarships, approve reviewers, assign applications to reviewers, and record final decisions.

## 2. Problem Statement

Scholarship workflows often involve several disconnected steps: collecting student information, managing eligibility details, receiving essays, assigning reviewers, tracking review completion, and recording final decisions. ScholarTrack brings these steps into one system with clear roles and stored records.

## 3. Target Users

- Students applying for scholarships.
- Reviewers evaluating student applications.
- Admins managing scholarship programs and decisions.

## 4. User Roles

### Student

Students can:
- register publicly
- verify email
- log in after verification
- complete a student profile
- browse scholarships
- submit scholarship applications
- submit essays and supporting content
- view their applications

### Reviewer

Reviewers can:
- register as reviewer applicants
- submit reviewer request details and a PDF resume
- wait for admin approval
- view assigned applications after approval
- read essays for assigned applications
- submit reviewer notes, scores, and rationale
- mark review as complete

### Admin

Admins can:
- create users
- approve or reject reviewer requests
- create, update, delete, and inspect scholarships
- view scholarship statistics
- view all applications
- assign reviewers
- record final decisions
- update and delete decisions

## 5. Key Workflows

### Student Registration And Verification

1. Student registers with name, email, password, role, and optional profile details.
2. Backend creates a user with `verified_email=False`.
3. Backend sends a verification link through the email service.
4. Student opens the verification page.
5. Backend marks the email as verified.
6. Student can log in.

### Scholarship Application

1. Student opens scholarships page.
2. Student filters or views available scholarships.
3. Student opens scholarship details.
4. Student submits an application.
5. Student submits essay and supporting content.
6. Application starts as `PENDING`.

### Reviewer Approval

1. Public user registers as `REVIEWER`.
2. Backend stores the account as `PENDING_REVIEWER`.
3. User submits reviewer request details and PDF resume.
4. Admin reviews pending reviewers.
5. Admin approves or rejects.
6. Approved reviewer can log in as `REVIEWER`.

### Review

1. Admin assigns reviewer to an application.
2. Application status becomes `UNDER_REVIEW`.
3. Reviewer opens assigned application.
4. Reviewer reads essay and details.
5. Reviewer submits note, score, and rationale.
6. Reviewer completes review.
7. Application status becomes `REVIEW_DONE`.

### Decision

1. Admin opens reviewed application.
2. Backend checks that review is complete.
3. Backend checks that a reviewer score exists.
4. Backend prevents duplicate decisions.
5. Admin records `AWARDED`, `SHORTLISTED`, or `REJECTED`.
6. Application status is synchronized with the decision.

## 6. Screens And Purpose

- Login page: authenticate existing users.
- Register page: register students and reviewer applicants.
- Verify email page: confirm email verification links.
- Scholarships page: list and filter scholarships.
- Scholarship detail page: inspect one scholarship.
- Application page: submit an application and essay.
- Student dashboard: view student applications and details.
- Student profile page: view or create student profile details.
- Reviewer request page: submit reviewer credentials and resume.
- Reviewer dashboard: review assigned applications and submit scores.
- Admin dashboard: main admin area with tabs and pending reviewer management.
- Admin home dashboard: summary counts.
- Admin users panel: list and inspect users.
- Admin scholarships panel: manage scholarships and view stats.
- Admin applications panel: assign reviewers and record decisions.
- Admin decisions panel: list, inspect, update, or delete decisions.

## 7. Backend Services

- Auth service: registration, login, password hashing, JWT creation.
- User service: fetch users.
- Student service: create/fetch profiles and application count.
- Scholarship service: scholarship CRUD, filters, and stats.
- Application service: create applications, prevent duplicates, assign reviewers, complete reviews, merge application details.
- Essay service: create and fetch MongoDB essays.
- Reviewer note service: create and fetch MongoDB reviewer notes.
- Decision service: enforce decision rules and synchronize application status.
- Email service: generate verification token and print verification email content.

## 8. API Summary

Authentication:
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/verify-email`
- `POST /auth/reviewer-request`

Users and students:
- `GET /users/`
- `GET /users/{user_id}`
- `POST /students/`
- `GET /students/{student_id}`

Scholarships:
- `POST /scholarships/`
- `GET /scholarships/`
- `GET /scholarships/{scholarship_id}`
- `GET /scholarships/{scholarship_id}/stats`
- `PATCH /scholarships/{scholarship_id}`
- `DELETE /scholarships/{scholarship_id}`

Applications:
- `POST /applications/`
- `GET /applications/`
- `GET /applications/{application_id}`
- `GET /applications/student/{student_id}`
- `GET /applications/reviewer/{reviewer_id}`
- `PATCH /applications/{application_id}/assign`
- `PATCH /applications/{application_id}/review`
- `POST /applications/{application_id}/review`
- `PATCH /applications/{application_id}/decision`

Mongo-backed content:
- `POST /essays/`
- `GET /essays/{application_id}`
- `POST /reviewer-notes/`
- `GET /reviewer-notes/{application_id}`

Admin:
- `POST /admin/users`
- `GET /admin/decisions`
- `POST /admin/decisions`
- `GET /admin/decisions/{decision_id}`
- `GET /admin/applications/{application_id}/decision`
- `PATCH /admin/decisions/{decision_id}`
- `DELETE /admin/decisions/{decision_id}`
- `GET /admin/pending-reviewers`
- `GET /admin/reviewers`
- `PATCH /admin/users/{user_id}/approve-reviewer`
- `PATCH /admin/users/{user_id}/reject-reviewer`
- `GET /admin/reviewer-requests/{user_id}/resume`

## 9. Database Summary

PostgreSQL stores structured relational data:
- users
- students
- scholarships
- applications
- decisions
- reviewer_requests

Application status is stored in PostgreSQL because it is part of the main relational workflow.

## 10. MongoDB Usage

MongoDB stores longer, flexible application-related content:
- essays
- reviewer notes

These are stored as Beanie documents because they are document-like records connected to an application by `application_id`.

## 11. Security Features

- JWT authentication.
- Password hashing with bcrypt.
- Password length validation.
- Email verification before login.
- Public registration blocked from creating admin accounts.
- Reviewer accounts require admin approval.
- Role guards for admin, student, and reviewer routes.
- Student ownership checks for profiles and applications.
- Reviewer assignment checks for application and note access.
- Rate limiting on register and login.
- Global error handler for consistent error responses.

## 12. Business Rules

- Public users can register only as students or reviewer applicants.
- Reviewer applicants become `PENDING_REVIEWER`.
- Pending reviewers cannot log in until approved.
- Students must verify email before login.
- A student cannot apply twice to the same scholarship.
- Admin creates and manages scholarships.
- Admin assigns reviewers.
- Reviewers can only view assigned applications.
- A decision can only be created after review completion and a review score.
- Only one decision can exist for an application.
- Reviewer notes are hidden from students until a decision is recorded.
- Scholarship stats count application statuses from PostgreSQL.

## 13. Future Enhancements

- Replace console-style email output with a real email provider.
- Decide whether Alembic or SQLAlchemy `create_all` is the official schema strategy.
- Improve cross-database consistency between PostgreSQL and MongoDB writes.
- Add typed nested schemas for application details.
- Add stronger password rules beyond length.
- Add pagination to every list endpoint.
- Add production deployment manifests.
- Add frontend route guards based on JWT role.
- Add refresh tokens or token rotation.
- Add audit logs for admin decisions.
