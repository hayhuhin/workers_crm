from django.urls import path,include
from django.contrib.auth import views
from . import views as user_view
from rest_framework.authtoken import views



urlpatterns = [
    path('login',user_view.UserLogin.as_view()),
    path('register',user_view.AdminUserRegister.as_view()),
    path('logout',user_view.UserLogout.as_view()),
    path('user',user_view.UserView.as_view()),
    path('create_user',user_view.CreateUser.as_view()),
    path('assign/finance/full',user_view.AssignFinanceFullPermission.as_view()),
    path('assign/finance/view',user_view.AssignFinanceViewPermission.as_view()),
    path('assign/finance/update',user_view.AssignFinanceUpdatePermission.as_view()),
    path('disallow/finance/full',user_view.DisallowFinanceFullPermission.as_view()),
    path('disallow/finance/view',user_view.DisallowFinanceViewPermission.as_view()),
    path('disallow/finance/update',user_view.DisallowFinanceUpdatePermission.as_view()),

]