from django.contrib import admin
from django.urls import path,include
from . import views as company_views



urlpatterns = [
    path("create",company_views.CreateCompany.as_view(),name="create_company"),
    path("delete",company_views.DeleteCompany.as_view(),name="delete_company"),

]