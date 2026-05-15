from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from api.database import get_db
from api import models
from api.dependencies import get_current_user, get_team_member

router = APIRouter(tags=["tasks"])


def task_dict(t: models.Task):
    return {"id": t.id, "team_id": t.team_id, "title": t.title, "status": t.status,
            "creator_id": t.creator_id, "assignee_id": t.assignee_id, "created_at": t.created_at}


class CreateTaskRequest(BaseModel):
    title: str
    assignee_id: Optional[int] = None


class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    assignee_id: Optional[int] = None


class UpdateStatusRequest(BaseModel):
    status: str


@router.get("/api/teams/{team_id}/tasks")
def list_tasks(team_id: int, filter: Optional[str] = Query(None),
               db: Session = Depends(get_db), current_user: models.User = Depends(get_team_member)):
    q = db.query(models.Task).filter(models.Task.team_id == team_id)
    if filter == "me":
        q = q.filter(models.Task.assignee_id == current_user.id)
    elif filter == "unassigned":
        q = q.filter(models.Task.assignee_id == None)
    return [task_dict(t) for t in q.order_by(models.Task.created_at.desc()).all()]


@router.post("/api/teams/{team_id}/tasks", status_code=201)
def create_task(team_id: int, body: CreateTaskRequest,
                db: Session = Depends(get_db), current_user: models.User = Depends(get_team_member)):
    if not 1 <= len(body.title) <= 100:
        raise HTTPException(400, detail={"code": "VALIDATION_ERROR", "message": "태스크 제목은 1-100자여야 합니다"})
    task = models.Task(team_id=team_id, title=body.title, creator_id=current_user.id, assignee_id=body.assignee_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task_dict(task)


@router.get("/api/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(404, detail={"code": "NOT_FOUND", "message": "태스크를 찾을 수 없습니다"})
    if current_user.team_id != task.team_id:
        raise HTTPException(403, detail={"code": "FORBIDDEN", "message": "이 팀의 멤버가 아닙니다"})
    return task_dict(task)


@router.put("/api/tasks/{task_id}")
def update_task(task_id: int, body: UpdateTaskRequest,
                db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(404, detail={"code": "NOT_FOUND", "message": "태스크를 찾을 수 없습니다"})
    if current_user.team_id != task.team_id:
        raise HTTPException(403, detail={"code": "FORBIDDEN", "message": "이 팀의 멤버가 아닙니다"})
    if body.title is not None:
        if not 1 <= len(body.title) <= 100:
            raise HTTPException(400, detail={"code": "VALIDATION_ERROR", "message": "태스크 제목은 1-100자여야 합니다"})
        task.title = body.title
    if body.assignee_id is not None:
        task.assignee_id = body.assignee_id
    db.commit()
    db.refresh(task)
    return task_dict(task)


@router.patch("/api/tasks/{task_id}/status")
def update_task_status(task_id: int, body: UpdateStatusRequest,
                       db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if body.status not in ("TODO", "DOING", "DONE"):
        raise HTTPException(400, detail={"code": "VALIDATION_ERROR", "message": "status는 TODO, DOING, DONE 중 하나여야 합니다"})
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(404, detail={"code": "NOT_FOUND", "message": "태스크를 찾을 수 없습니다"})
    if current_user.team_id != task.team_id:
        raise HTTPException(403, detail={"code": "FORBIDDEN", "message": "이 팀의 멤버가 아닙니다"})
    task.status = body.status
    db.commit()
    return {"id": task.id, "status": task.status}


@router.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(404, detail={"code": "NOT_FOUND", "message": "태스크를 찾을 수 없습니다"})
    if current_user.team_id != task.team_id:
        raise HTTPException(403, detail={"code": "FORBIDDEN", "message": "이 팀의 멤버가 아닙니다"})
    team = db.query(models.Team).filter(models.Team.id == task.team_id).first()
    if task.creator_id != current_user.id and team.owner_id != current_user.id:
        raise HTTPException(403, detail={"code": "FORBIDDEN", "message": "권한이 없습니다"})
    db.delete(task)
    db.commit()
    return {}
