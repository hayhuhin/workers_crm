from django.urls import path
from dashboard import views as dashboard_views



urlpatterns = [
    path('test',dashboard_views.index),
    path('dashboard',dashboard_views.dashboard),
    path('teams',dashboard_views.teams),
]
