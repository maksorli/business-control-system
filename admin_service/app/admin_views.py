from sqladmin import ModelView
from app.models.team import Team  
from app.models.user import User

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.role, User.created_at]

class TeamAdmin(ModelView, model=Team):
    column_list = [Team.id, Team.name, Team.created_at]
