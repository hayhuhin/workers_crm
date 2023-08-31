from django.urls import path,include
from . import views as user_view



urlpatterns = [
    path('',user_view.home),
    path('',include('django.contrib.auth.urls')),
    path('sign',user_view.sign_up),

]