from enum import Enum


class UserRole(str, Enum):
    STUDENT = "STUDENT"
    REVIEWER = "REVIEWER"
    ADMIN = "ADMIN"


class ApplicationStatus(str, Enum):
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    SHORTLISTED = "SHORTLISTED"
    REJECTED = "REJECTED"
    AWARDED = "AWARDED"


class DecisionStatus(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    WAITLISTED = "WAITLISTED"