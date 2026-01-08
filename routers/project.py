from fastapi import APIRouter,Depends
from sqlmodel import Session,select

from database import get_session
from models.project import Project
from models.user import User
from dependencies.auth import get_current_user
from schemas.project import ProjectResponse
from typing import Optional,Annotated
from fastapi import Body
from schemas.project import ProjectCreate


router = APIRouter(
    prefix="/projects",
    tags= ["Projects"]
    )


# CREATE A PROJECT(PROTECTED).

@router.post("/",response_model = ProjectResponse)
def create_project(
    data : ProjectCreate,
    session : Session = Depends(get_session),
    current_user : User = Depends(get_current_user)
):
    project = Project(
        name = data.name,
        description = data.description,
        owner_id = current_user.id
    )

    session.add(project)
    session.commit()
    session.refresh(project)

    return project


# LIST OF MY PROJECTS(PROTECTED).

@router.get("/",response_model = list[ProjectResponse])
def list_of_projects(
    session : Session = Depends(get_session),
    current_user : User = Depends(get_current_user)
):
    
    projects = session.exec(
        select(Project).where(Project.owner_id == current_user.id)
    ).all()

    return projects

    



