from fastapi import APIRouter,Depends,HTTPException
from sqlmodel import Session,select

from database import get_session
from models.task import Task
from models.project import Project
from models.user import User
from dependencies.auth import get_current_user
from schemas.task import TaskResponse
from typing import Optional
from fastapi import Body
from schemas.task import TaskCreate
from schemas.task import TaskUpdate
from fastapi import Query
from models.project_member import ProjectMember
from core.enums import TaskStatus

router = APIRouter(prefix="/task",
                   tags=["task"]
                )


# CREATE TASK IN PROJECT(PROTECTED).

@router.post("/",response_model = TaskResponse)
def create_task(
    data : TaskCreate,
    session : Session = Depends(get_session),
    current_user : User = Depends(get_current_user)
):
    
    project = session.get(Project,data.project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail= "Project not found."
        )
    
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code= 403,
            detail= "Not allowed to creater tasks for this project."
        )
    

    task = Task(
        title = data.title,
        description = data.description,
        project_id = data.project_id,
        created_by = current_user.id
         )
    

    session.add(task)
    session.commit()
    session.refresh(task)

    return task



# READ TASK FROM PROJECT(PROTECTED).

@router.get("/project/{project_id}",response_model = list[TaskResponse])
def list_tasks_for_project(
    project_id : int,
    limit : Optional[int] = Query(10,ge=0,le=50),
    offset : Optional[int] = Query(0,ge=0,),
    status : Optional[TaskStatus] = Query(default=None),
    assigned_to : Optional[str] = Query(default=None),
    session : Session = Depends(get_session),
    current_user : User = Depends(get_current_user)
):
    
    project = session.get(Project,project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found."
        )
    
    is_member = session.exec(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == current_user.id
        )
    ).first()
    
    if project.owner_id != current_user.id and not is_member:
        raise HTTPException(
            status_code=403,
            detail="Not allowed to read tasks from the project."
        )
    
    query = select(Task).where(Task.project_id==project_id)

    if status is not None:
        query = query.where(Task.status==status)

    if assigned_to is not None:
        query = query.where(Task.assigned_to==assigned_to)

    
    tasks = session.exec(query.offset(offset).limit(limit)).all()

    return tasks


@router.patch("/{task_id}",response_model= TaskResponse)
def task_update(
    task_id : int,
    data : TaskUpdate,
    session : Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    
    task = session.get(Task,task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail = "Task not Found."
        )
    
    project = session.get(Project,task.project_id)

    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code = 403,
            detail = "Not allowed to update this task."
        )
    
    if data.status is not None:
        task.status = data.status

    if data.assigned_to is not None:
        task.assigned_to = data.assigned_to

        session.add(task)
        session.commit()
        session.refresh(task)
        return task
        
