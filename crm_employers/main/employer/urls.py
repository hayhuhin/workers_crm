from django.urls import path,include
from django.contrib.auth import views
from rest_framework.authtoken import views
from . import views as employer_views
from .profile import views as profile_views
from .department import views as department_views
from .department.department_task import views as department_task_views
from .leads import views as lead_views
from .task import views as task_views


urlpatterns = [
    #high permission routes
    path('employer/create',employer_views.CreateEmployer.as_view()),
    path('employer/delete',employer_views.DeleteEmployer.as_view()),
    path('employer/update',employer_views.UpdateEmployer.as_view()),
    path('employer/get',employer_views.GetEmployer.as_view()),
    
    #high permission router
    path('department/create',department_views.CreateDepartment.as_view()),
    path('department/delete',department_views.DeleteDepartment.as_view()),
    path('department/update',department_views.UpdateDepartment.as_view()),
    path('department/get',department_views.GetDepartment.as_view()),
    
    #normal permission routes
    path('employer/profile/get',profile_views.GetProfile.as_view()),
    path('employer/profile/update',profile_views.UpdateProfile.as_view()),



    # #leads employer permission routes
    path('employer/lead/create',lead_views.CreateLead.as_view()),
    path('employer/lead/delete',lead_views.DeleteLead.as_view()),
    path('employer/lead/update',lead_views.UpdateLead.as_view()),
    path('employer/lead/get',lead_views.GetLead.as_view()),

    # employer task routes
    path('employer/task/create',task_views.CreateTask.as_view()),
    path('employer/task/delete',task_views.DeleteTask.as_view()),
    path('employer/task/update',task_views.UpdateTask.as_view()),
    path('employer/task/get',task_views.GetTask.as_view()),

    # department task routes
    path('department/task/create',department_task_views.CreateTask.as_view()),
    path('department/task/delete',department_task_views.DeleteTask.as_view()),
    path('department/task/update',department_task_views.UpdateTask.as_view()),
    path('department/task/get',department_task_views.GetTask.as_view()),
]