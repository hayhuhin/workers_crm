from django.urls import path,include
from django.contrib.auth import views
from . import views as employer_views
from rest_framework.authtoken import views



urlpatterns = [
    path('create',employer_views.CreateEmployer.as_view()),
    path('delete',employer_views.DeleteEmployer.as_view()),
    path('update',employer_views.UpdateEmployer.as_view()),
    path('get',employer_views.GetEmployer.as_view()),
    path('profile/get',employer_views.GetProfile.as_view()),
    path('profile/update',employer_views.UpdateProfile.as_view()),
]