from django.urls import path
from dashboard import views as dashboard_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('test',dashboard_views.index),
    path('dashboard',dashboard_views.dashboard),
    path('teams',dashboard_views.teams),
    path('personal_tasks',dashboard_views.personal_tasks),
    path('daily_tasks',dashboard_views.daily_tasks),
    path('profile',dashboard_views.profile),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
