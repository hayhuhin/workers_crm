from django.contrib import admin
from django.urls import path,include




urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/api/user/',include('user.urls')),
    path('v1/api/finance/',include('finance.urls')),
    path('v1/api/',include('employer.urls')),
    path('v1/api/dashboard',include('dashboard.urls')),




]
