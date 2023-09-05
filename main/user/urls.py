from django.urls import path,include
from django.contrib.auth import views
from . import views as user_view
from  .forms import UserLoginForm




urlpatterns = [
    path('',user_view.home),
    path('',include('django.contrib.auth.urls')),
    path('sign',user_view.sign_up),
    path('login',views.LoginView.as_view(
        template_name = 'registration/login.html',
        authentication_form = UserLoginForm),
        )
]