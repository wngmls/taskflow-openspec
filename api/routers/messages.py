from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from api.database import get_db
from api import models
from api.dependencies import get_current_user, get_team_member

router = APIRouter(tags=["messages"])


def msg_dict(m: models.Message):
    return {"id": m.id, "user_id": m.user_id, "user_email": m.user.email,
            "content": m.content, "created_at": m.created_at}


class CreateMessageRequest(BaseModel):
    content: str


@router.get("/api/teams/{team_id}/messages")
def list_messages(team_id: int, since: Optional[str] = Query(None),
                  db: Session = Depends(get_db), current_user: models.User = Depends(get_team_member)):
    q = db.query(models.Message).filter(models.Message.team_id == team_id)
    if since:
        try:
            since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
            q = q.filter(models.Message.created_at > since_dt)
        except ValueError:
            raise HTTPException(400, detail={"code": "VALIDATION_ERROR", "message": "since 형식이 올바르지 않습니다"})
        return [msg_dict(m) for m in q.order_by(models.Message.created_at.asc()).all()]
    return [msg_dict(m) for m in q.order_by(models.Message.created_at.desc()).limit(50).all()][::-1]


@router.post("/api/teams/{team_id}/messages", status_code=201)
def create_message(team_id: int, body: CreateMessageRequest,
                   db: Session = Depends(get_db), current_user: models.User = Depends(get_team_member)):
    if len(body.content) > 1000:
        raise HTTPException(400, detail={"code": "TOO_LONG", "message": "메시지는 1000자 이내로 입력하세요",
                                         "limit": 1000, "actual": len(body.content)})
    if len(body.content) == 0:
        raise HTTPException(400, detail={"code": "VALIDATION_ERROR", "message": "메시지를 입력해주세요"})
    msg = models.Message(team_id=team_id, user_id=current_user.id, content=body.content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg_dict(msg)


@router.delete("/api/messages/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    msg = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not msg:
        raise HTTPException(404, detail={"code": "NOT_FOUND", "message": "메시지를 찾을 수 없습니다"})
    if msg.user_id != current_user.id:
        raise HTTPException(403, detail={"code": "NOT_OWNER", "message": "본인의 메시지만 삭제할 수 있습니다"})
    db.delete(msg)
    db.commit()
    return {}
