import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from api.database import get_db
from api import models, auth as auth_utils
from api.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class SignupRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


def user_response(user: models.User, token: str):
    return {"token": token, "user": {"id": user.id, "email": user.email, "team_id": user.team_id}}


@router.post("/signup", status_code=201)
def signup(body: SignupRequest, db: Session = Depends(get_db)):
    if not EMAIL_RE.match(body.email):
        raise HTTPException(400, detail={"code": "VALIDATION_ERROR", "message": "올바른 이메일 형식이 아닙니다"})
    if len(body.password) < 8:
        raise HTTPException(400, detail={"code": "VALIDATION_ERROR", "message": "8자 이상 입력해주세요"})
    if db.query(models.User).filter(models.User.email == body.email).first():
        raise HTTPException(409, detail={"code": "EMAIL_TAKEN", "message": "이미 가입된 이메일입니다"})
    user = models.User(email=body.email, password_hash=auth_utils.hash_password(body.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user_response(user, auth_utils.create_token(user.id))


@router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == body.email).first()
    if not user or not auth_utils.verify_password(body.password, user.password_hash):
        raise HTTPException(401, detail={"code": "INVALID_CREDENTIALS", "message": "이메일 또는 비밀번호가 일치하지 않습니다"})
    return user_response(user, auth_utils.create_token(user.id))


@router.post("/logout")
def logout():
    return {}


@router.get("/me")
def me(current_user: models.User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "team_id": current_user.team_id}
