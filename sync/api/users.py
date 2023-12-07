from fastapi import APIRouter, HTTPException, status, Depends
from typing import List , Annotated
from pydantic import Field
from sqlalchemy.orm import Session 
from sqlalchemy import select , update , delete

from schemas import users as UserSchema
from database.generic import get_db
from models.users import User as UserModel
from api.depends import check_user_id, pagination_parms, test_verify_token
from crud import users as UserCrud

db_session:Session = get_db()
router = APIRouter(tags=["users"], prefix="/api", dependencies=[Depends(test_verify_token)])

@router.get("/users", response_model=List[UserSchema.UserRead], response_description="Get list of user")
def get_users(page_parms:dict=Depends(pagination_parms)):
    users = UserCrud.get_users(**page_parms)
    return users

@router.post("/userCreate" , deprecated=True)
def create_user_deprecated(newUser: UserSchema.UserCreate ):
    return "deprecated"

@router.get("/users/{user_id}", response_model=UserSchema.UserRead )
def get_user_by_id(qry: str = None, user_id: int = Depends(check_user_id)):

    user = UserCrud.get_user_by_id(user_id)
    if user:
        return user
        
    raise HTTPException(status_code=404, detail="User not found")
    
@router.post("/users" , response_model=UserSchema.UserCreateResponse, status_code=201 )
def create_users(newUser: UserSchema.UserCreate ):
    """
    Create an user with the following information:

    - **name**
    - **password**
    - **age**
    - **birthday**
    - **email**
    - **avatar** (optional)

    """
    user = UserCrud.get_user_id_by_email(newUser.email)
    if user:
        raise HTTPException(status_code=409, detail=f"User already exists")
    
    user = UserCrud.create_user(newUser)

    return vars(user)

@router.delete("/users/{user.id}",status_code=status.HTTP_204_NO_CONTENT )
def delet_users(user_id: int = Depends(check_user_id)):
    UserCrud.delete_user(user_id)
    return

@router.put("/users/{user_id}" , response_model=UserSchema.UserUpdateResponse )
def update_user(newUser: UserSchema.UserUpdate, user_id: int = Depends(check_user_id) ):
    UserCrud.update_user(newUser,user_id)

    return newUser

@router.put("/users/{user_id}/password", status_code=status.HTTP_204_NO_CONTENT)
def update_user_password( newUser:UserSchema.UserUpdatePassword, user_id: int = Depends(check_user_id)):
    UserCrud.update_user_password(newUser,user_id)  
    return 