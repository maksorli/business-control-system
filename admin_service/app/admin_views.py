from sqladmin import ModelView
from app.models.team import Team  
from app.models.user import User
from app.models.department import Department
from app.models.task import Task
from app.models.comment import Comment

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.role, User.created_at]

class TeamAdmin(ModelView, model=Team):
    column_list = [Team.id, Team.name, Team.invite_code, Team.created_at]

class DepartmentAdmin(ModelView, model=Department):
    column_list = [Department.id, Department.name, Department.created_at]

class TaskAdmin(ModelView, model=Task):
    column_list = [Task.id, Task.assignee_id, Task.team_id, Task.title, Task.created_at]

class CommentAdmin(ModelView, model=Comment):
    column_list = [Comment.id, Comment.content,  Comment.task_id,Comment.user_id, Comment.created_at]