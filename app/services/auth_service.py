from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token, create_refresh_token, decode_token


class AuthService:
    @staticmethod
    def register(db: Session, data):
        if db.scalar(select(User).where(User.email == data.email)):
            raise HTTPException(400, "Email already registered")
        # Public registration creates Customer accounts only.
        user = User(
            name=data.name,
            email=data.email,
            phone=data.phone,
            password_hash=hash_password(data.password),
            role=data.role.value,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def login(db: Session, email: str, password: str):
        user = db.scalar(select(User).where(User.email == email))
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(401, "Invalid email or password")
        if not user.is_active:
            raise HTTPException(403, "Account is inactive")
        return {
            "access_token": create_access_token(user.id, user.role),
            "refresh_token": create_refresh_token(user.id, user.role),
            "token_type": "bearer",
        }

    @staticmethod
    def refresh(db: Session, refresh_token: str):
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(401, "Refresh token required")
        user = db.get(User, int(payload["sub"]))
        if not user or not user.is_active:
            raise HTTPException(401, "Invalid user")
        return {
            "access_token": create_access_token(user.id, user.role),
            "refresh_token": create_refresh_token(user.id, user.role),
            "token_type": "bearer",
        }
