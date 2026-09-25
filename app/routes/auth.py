from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import RegisterRequest, UserResponse, TokenResponse, RefreshRequest, ChangePasswordRequest
from app.services.auth_service import AuthService
from app.utils.security import verify_password, hash_password
from app.utils.jwt import decode_token, create_access_token, create_refresh_token

router=APIRouter(prefix="/auth",tags=["Authentication"])


@router.post("/register",response_model=UserResponse,status_code=201)
def register(data:RegisterRequest,db:Session=Depends(get_db)):
    return AuthService.register(db,data)


@router.post("/login",response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    return AuthService.login(db,form_data.username,form_data.password)


@router.post("/refresh",response_model=TokenResponse)
def refresh(data:RefreshRequest,db:Session=Depends(get_db)):
    return AuthService.refresh(db,data.refresh_token)


@router.get("/me",response_model=UserResponse)
def me(current_user:User=Depends(get_current_user)):
    return current_user


@router.put("/change-password")
def change_password(data:ChangePasswordRequest,current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    if not verify_password(data.current_password,current_user.password_hash):
        raise HTTPException(400,"Current password is incorrect")
    current_user.password_hash=hash_password(data.new_password)
    db.commit()
    return {"message":"Password changed successfully"}
