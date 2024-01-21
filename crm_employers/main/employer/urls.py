from django.urls import path,include
from django.contrib.auth import views
from . import views as employer_views
from rest_framework.authtoken import views



urlpatterns = [
    path('profile/add',employer_views.AddProfile.as_view()),
    path('profile/delete',employer_views.DeleteProfile.as_view()),
    # path('profile/Delte',employer_views.DeleteProfile.as_view()),
    path('profile/get',employer_views.GetProfile.as_view()),

]