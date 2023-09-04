from django.contrib import admin
from django.urls import path,include
from tasks import views as tasks_view



urlpatterns = [
    path('tasks',tasks_view.tasks)
]