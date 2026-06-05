# ScholarTrack Backend

## Overview

ScholarTrack Backend is a FastAPI-based scholarship management system that supports:

* JWT Authentication
* Role-Based Access Control
* Scholarship Management
* Student Applications
* Reviewer Workflow
* Decision Workflow
* PostgreSQL Database
* MongoDB Integration

---

# Tech Stack

* FastAPI
* PostgreSQL
* MongoDB
* SQLAlchemy
* Beanie ODM
* JWT Authentication
* Pytest
* Nginx

---

# Prerequisites

Install the following before running the project:

* Python 3.10+
* PostgreSQL
* MongoDB

---

# Setup Steps

### 1. Clone Repository

```bash
git clone <repository-url>

cd ScholarTrack/backend
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / Mac

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file inside the backend folder.

Example:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/scholartrack

MONGODB_URL=mongodb://localhost:27017

MONGODB_DATABASE=scholartrack

SECRET_KEY=your_secret_key

ALGORITHM=HS256
```

---

# Folder Structure

```text
backend/

├── app/
│   ├── config/
│   ├── middleware/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── tests/
│
├── requirements.txt
├── README.md
├── nginx.conf
└── setup.sh
```

---

# Run Application

Start FastAPI server:

```bash
uvicorn app.main:app --reload
```

Server URL:

```text
http://127.0.0.1:8000
```

---

# API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# Run Tests

```bash
pytest
```

Expected Output:

```text
6 passed
```

---

# Database Usage

### PostgreSQL

Stores:

* Users
* Students
* Scholarships
* Applications
* Decisions

### MongoDB

Stores:

* Essays
* Reviewer Notes

---

# Authentication

The system uses JWT Authentication.

Workflow:

1. Register User
2. Login User
3. Receive JWT Token
4. Pass Token in Authorization Header

Example:

```text
Authorization: Bearer <token>
```

---

# Nginx Reverse Proxy

Nginx configuration is available in:

```text
nginx.conf
```

Used to route incoming traffic to the FastAPI backend.

---

# Project Status

Backend Requirements Completed Successfully.

Features Tested Using Pytest.

Ready for Deployment.
