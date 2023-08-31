from django.contrib import admin
from django.contrib.auth.models import Group,User
from .models import Employer,Department

admin.site.unregister(Group)

class EmployerInline(admin.StackedInline):
    model = Employer

class UserAdmin(admin.ModelAdmin):
    model = User


    #displays it in the admin panel
    fields = ['username','password']
    inlines = [EmployerInline]

admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(Department)
