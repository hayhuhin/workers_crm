from django.contrib import admin
from django.contrib.auth.models import Group,Permission
from .models import User

from employer.models import Employer,Department,Lead,DepartmentTask,Task
# from dashboard.models import Income,GraphPermission

admin.site.unregister(Group)

class EmployerInline(admin.StackedInline):
    model = Employer

class UserAdmin(admin.ModelAdmin):
    model = User


    #displays it in the admin panel
    fields = ['username','password']
    inlines = [EmployerInline]


admin.site.register(User,UserAdmin)
admin.site.register(Department)
admin.site.register(Lead)
admin.site.register(Task)
admin.site.register(DepartmentTask)
# admin.site.register(Income)
# admin.site.register(GraphPermission)
admin.site.register(Group)
admin.site.register(Permission)


