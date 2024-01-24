from django.urls import path,include
from django.contrib.auth import views
from . import views as user_view
from rest_framework.authtoken import views



urlpatterns = [
    path('login',user_view.UserLogin.as_view()),
    path('register',user_view.UserRegister.as_view()),
    path('logout',user_view.UserLogout.as_view()),
    path('user',user_view.UserView.as_view()),
    path('assign/finance/full',user_view.AssignFinanceFullPermission.as_view()),
    # path('user/assign/finance/full',user_view.AssignFinanceFullPermission.as_view()),
    # path('user/assign/finance/full',user_view.AssignFinanceFullPermission.as_view()),
    # path('user/assign/finance/full',user_view.AssignFinanceFullPermission.as_view()),

]