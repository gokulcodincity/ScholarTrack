from enum import Enum


class UserRole(str, Enum):
    STUDENT = "STUDENT"
    REVIEWER = "REVIEWER"
    ADMIN = "ADMIN"


class ApplicationStatus(str, Enum):
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    REVIEW_DONE = "REVIEW_DONE"
    SHORTLISTED = "SHORTLISTED"
    REJECTED = "REJECTED"
    AWARDED = "AWARDED"


class DecisionStatus(str, Enum):
    AWARDED = "AWARDED"
    SHORTLISTED = "SHORTLISTED"
    REJECTED = "REJECTED"