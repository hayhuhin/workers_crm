from django.urls import path,include
from django.contrib.auth import views
from . import views as employer_views
from .profile import views as profile_views
from .department import views as department_views
from rest_framework.authtoken import views



urlpatterns = [
    path('employer/create',employer_views.CreateEmployer.as_view()),
    path('employer/delete',employer_views.DeleteEmployer.as_view()),
    path('employer/update',employer_views.UpdateEmployer.as_view()),
    path('employer/get',employer_views.GetEmployer.as_view()),
    path('employer/profile/get',profile_views.GetProfile.as_view()),
    path('employer/profile/update',profile_views.UpdateProfile.as_view()),
    path('department/create',department_views.CreateDepartment.as_view()),
]