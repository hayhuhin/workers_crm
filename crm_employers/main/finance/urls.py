from django.urls import path,include
from . import views as income_views
from .customer import views as customer_views

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
    path("customer/create",customer_views.CreateCustomerView.as_view()),
    path("customer/delete",customer_views.DeleteCustomerView.as_view()),
    path("customer/update",customer_views.UpdateCustomerView.as_view()),
    path("customer/get",customer_views.GetCustomerView.as_view()),








]