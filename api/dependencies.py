from fastapi import Depends, HTTPException, Header
from jose import JWTError
from sqlalchemy.orm import Session
from api.database import get_db
from api import models, auth


def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)) -> models.User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, detail={"code": "TOKEN_EXPIRED", "message": "인증이 만료되었습니다"})
    token = authorization[7:]
    try:
        user_id = auth.decode_token(token)
    except JWTError:
        raise HTTPException(401, detail={"code": "TOKEN_EXPIRED", "message": "인증이 만료되었습니다"})
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(401, detail={"code": "TOKEN_EXPIRED", "message": "인증이 만료되었습니다"})
    return user


def get_team_member(team_id: int, current_user: models.User = Depends(get_current_user)) -> models.User:
    if current_user.team_id != team_id:
        raise HTTPException(403, detail={"code": "FORBIDDEN", "message": "이 팀의 멤버가 아닙니다"})
    return current_user
