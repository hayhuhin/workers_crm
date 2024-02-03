from django.urls import path,include
from . import views as income_views
from .clients import views as client_views

urlpatterns = [
    #* income operation routes
    path("income/create",income_views.CreateIncome.as_view()),
    path("income/delete",income_views.DeleteIncome.as_view()),
    path("income/update",income_views.UpdateIncome.as_view()),
    path("income/get",income_views.GetIncome.as_view()),
    
    #* outcome operation routes 
    path("outcome/create",income_views.CreateOutcome.as_view()),
    path("outcome/delete",income_views.DeleteOutcome.as_view()),
    path("outcome/update",income_views.UpdateOutcome.as_view()),
    path("outcome/get",income_views.GetOutcome.as_view()),

    #* client operation routes
    path("client/create",client_views.CreateClientView.as_view()),
    path("client/delete",client_views.DeleteClientView.as_view()),
    path("client/update",client_views.UpdateClientView.as_view()),
    path("client/get",client_views.GetClientView.as_view()),







]