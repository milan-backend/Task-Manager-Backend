from fastapi import APIRouter,HTTPException,Depends
from sqlmodel import Session,select

from database import get_session
from models.project import Project
from models.user import User
from models.project_member import ProjectMember
from dependencies.auth import get_current_user
from schemas.project_member import ProjectMemberCreate


router = APIRouter(prefix="/projects/{project_id}/members",
                   tags=["Project Members"]
     )

#  ADD A MEMEBER

@router.post("/")
def add_member(
    project_id : int,
    data : ProjectMemberCreate,
    session : Session = Depends(get_session),
    current_user : User = Depends(get_current_user),
):
    
    project = session.get(Project,project_id)

    if not project:
        raise HTTPException(
            status_code= 404,
            detail = "Project not found."
        )

    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail = "Only project owner can add member."
        )
    
    existing_member = session.exec(
        select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == data.user_id
        )
    ).first()


    if existing_member:
        raise HTTPException(
            status_code = 400,
            detail = "User already a member"
        )
    
    user = session.get(User,data.user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail = "User not found"
        )
    

    member = ProjectMember(
        project_id = project_id,
        user_id = data.user_id
    )

    session.add(member)
    session.commit()
    session.refresh(member)

    return {"message": "User added to project."}
