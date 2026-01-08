from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from database import create_db_and_tables
from models.user import User
from models.refresh_token import RefreshToken
from models.project import Project
from models.task import Task
from models.project_member import ProjectMember

from routers.auth import router as auth_router
from routers.project import router as project_router
from routers.task import router as task_router
from routers.project_member import router as project_member_router

app = FastAPI()

@app.on_event("startup")
def on_event():
    create_db_and_tables()

app.include_router(auth_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(project_member_router)

