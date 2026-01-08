#  Task Management Backend (FastAPI)

A **production-style backend API** built using **FastAPI** that supports authentication, authorization, project collaboration, task management, and secure token handling.

This project focuses on **real backend fundamentals**, not just CRUD — including JWT authentication, refresh tokens, role-based access logic, pagination, and clean API design.

---

##  Features

###  Authentication & Security

- User signup & login
- JWT **access token** authentication
- **Refresh token** mechanism for better user experience
- Password hashing (no plain-text passwords)
- Protected routes using HTTP Bearer tokens
- Token revocation support

---

###  Authorization

- Project-based access control
- Only project owners can:
  - add members
  - manage project settings
- Members can collaborate within allowed projects
- Strict backend-side validation (no client trust)

---

###  Project Management

- Create projects
- List user-owned projects
- Add members to projects
- Many-to-many relationship between users and projects

---

###  Task Management

- Create tasks inside projects
- Update tasks using `PATCH` (partial updates)
- Assign tasks to users
- Track task status (`TODO`, `IN_PROGRESS`, `DONE`)
- Filter and paginate tasks
- Secure access to tasks based on project membership

---

##  Database & Migrations

- **SQLite** is used for development and demonstration purposes
- Database schema changes are handled using **Alembic migrations**
- Enum-like validation is enforced at the API level (SQLite limitation)
- Designed so it can be easily migrated to **PostgreSQL** in future projects

---

##  Testing

- All endpoints were **manually tested** using:
  - Swagger UI
  - Postman
- Authentication, authorization, and edge cases were verified manually

---

##  Deployment

- Backend deployed on **Render**
- Environment variables used for secrets
- SQLite used as demo database

> **Note:** SQLite database resets on redeploy.  
> This project is intended as a backend demo, not production data storage.

---

## 🛠 Tech Stack

- **FastAPI**
- **SQLModel**
- **SQLite**
- **JWT (python-jose)**
- **Passlib (bcrypt)**
- **Alembic**
- **Python-dotenv**

---

##  Learning Outcomes

Through this project, I learned:

- How JWT authentication works (access vs refresh tokens)
- Secure backend authorization patterns
- Proper API design (`PUT` vs `PATCH`)
- Pagination and filtering
- One-to-many & many-to-many relationships
- Database migrations with Alembic
- SQLite limitations vs PostgreSQL
- Real-world backend debugging and design decisions

---

##  Future Improvements

- Switch database to **PostgreSQL**
- Add automated tests (pytest)
- Add role-based permissions (admin/user)
- Add async database support
- Improve deployment using Docker

---

##  Running Locally

```bash
git clone <repository-url>
cd task-manager-backend
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt


## 🚀 Running Locally

```bash
git clone https://github.com/milan-backed/Task-Manager-Backend.git
cd Task-Manager-Backend

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload

Once running, open:
API Docs: http://127.0.0.1:8000/docs
OpenAPI JSON: http://127.0.0.1:8000/openapi.json