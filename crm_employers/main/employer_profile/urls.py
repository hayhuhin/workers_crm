from django.urls import path
from employer_profile import views as profile_view

urlpatterns = [
    path('old_profile',profile_view.profile_page),

]