from django.contrib import admin
from django.urls import path,include




urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/api/user/',include('user.urls')),
    path('v1/api/dashboard/',include('dashboard.urls')),
    path('',include('teams.urls')),
    path('',include('employer_profile.urls')),
    path('',include('tasks.urls')),



]
