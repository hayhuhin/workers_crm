from django.urls import path,include
from teams import views as team_view

urlpatterns = [
    path('teams',team_view.teams)
]
