from fastapi import APIRouter, HTTPException, status
from typing import List , Dict

from schemas import users as UserSchema
from database.fake_db import get_db

fake_db = get_db()

router = APIRouter(tags=["users"], prefix="/api")

@router.get("/users", response_model=List[UserSchema.UserRead], response_description="Get list of user")
def get_users(qry: str = None):
    """
    Create an user list with all the information:

    - **id**
    - **name**
    - **email**
    - **avatar**
    
    """
    return fake_db['users']

@router.post("/userCreate" , deprecated=True)
def create_user_deprecated(newUser: UserSchema.UserCreate ):
    return "deprecated"

@router.get("/users/{user_id}", response_model=UserSchema.UserRead )
def get_user_by_id(user_id: int, qry: str = None):
    for user in fake_db["users"]:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")
    
@router.post("/users" , response_model=UserSchema.UserCreateResponse, status_code=201 )
def create_users(user: UserSchema.UserCreate):
    fake_db["users"].append(user)
    return user

@router.delete("/users/{user.id}")
def delet_users(user_id: int):
    for user in fake_db["users"]:
        if user["id"] == user_id:
            fake_db["users"].remove(user)
            return user
    raise HTTPException(status_code=404, detail="User not found")
