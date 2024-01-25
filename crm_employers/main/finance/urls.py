from django.urls import path,include
from . import views as income_views

urlpatterns = [
    path("income/create",income_views.CreateIncome.as_view()),
    path("income/delete",income_views.DeleteIncome.as_view()),
]