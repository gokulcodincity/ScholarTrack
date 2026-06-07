from sqlalchemy.orm import Session
 
from app.models.user import User
from app.repositories.user_repository import UserRepository
 
 
def get_user_by_id(user_id: int, db: Session):
 
    user_repo = UserRepository(db)
    return user_repo.get_by_id(user_id)
 
 
def get_all_users(db: Session):
 
    user_repo = UserRepository(db)
    return user_repo.get_all()