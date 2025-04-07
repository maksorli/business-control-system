from fastapi import FastAPI
from sqladmin import Admin
from app.core.database import async_engine
from app.admin_views import UserAdmin, TeamAdmin, DepartmentAdmin, TaskAdmin, CommentAdmin

app = FastAPI()

 
admin = Admin(app, async_engine)
admin.add_view(UserAdmin)
admin.add_view(TeamAdmin)
admin.add_view(DepartmentAdmin)
admin.add_view(TaskAdmin)
admin.add_view(CommentAdmin)