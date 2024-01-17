from django.contrib import admin
from django.urls import path,include
from tasks import views as tasks_view



urlpatterns = [
    path('tasks',tasks_view.tasks,name='tasks'),
    path('edit-task/<int:ID>',tasks_view.Edit_Task,name='edit_task'),
    path('edit-lead/<int:ID>',tasks_view.Edit_lead,name='edit_lead'),


]