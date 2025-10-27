Name : B Sonali Priyadrasani 


Project Management Tool 

Project Overview : 
This backend is part of the Project Management Tool assignment.It allows users to manage projects, tasks, and teams with different roles such as Admin, Project Manager, and Developer.The application is built with FastAPI and MySQL, providing RESTful APIs for the frontend.

-> How to Run the Project
1.Clone or Extract Project

If you downloaded as ZIP:

unzip backend_project.zip
cd backend

2. Create a Virtual Environment
python -m venv venv

Activate it:
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

3️.Install Dependencies
pip install -r requirements.txt

4️. Configure Database
Open app/db.py and update your database credentials:

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://username:password@localhost/project_management"

Then create the database in MySQL:
CREATE DATABASE project_management;

5. Run the Server
uvicorn app.main:app --reload

6️. Open in Browser
Swagger Docs (API Testing UI):
http://127.0.0.1:8000/docs

->> API Endpoints Summary
User Management
Method Description
POST-Create new user
GET-Get all users
GET-{id}	Get user by ID
DELETE-{id}	Delete user

-->> Project Management
Create, edit, and delete projects.
Assign team members to projects.
Track project status and progress.

Method	Description
POST - Create new project
GET	- Get all projects
GET	- 	Get project by ID
PUT	- 	Update project
DELETE	- 	Delete project

-->> Task Management
Create, update, and delete tasks.
Assign tasks to specific users.
Set deadlines and status .
Automatic tracking of overdue tasks.

Method Description
POST - Create task
GET	- Get all tasks
GET	- 	Get task by ID
PUT	- 	Update task status/details
DELETE	- 	Delete task

-->>Authentication & Authorization
Login with role-based access control.
Secure routes per user role.

->>Assumptions
Each user has one of three roles: Admin, Manager, or Developer.
Only Admins can manage users.
Only Managers can create and assign projects/tasks.
Developers can only update task status and view assigned work.

Swagger UI: http://127.0.0.1:8000/docs

-->> Tools Used
Swagger → API Testing
GitHub → Version Control
VS Code → Development
MySQL Workbench → Database Management


For the E-R diagram, I have attached a document in this repository.The repository also includes database schema images and testing module screenshots for better understanding and verification.
