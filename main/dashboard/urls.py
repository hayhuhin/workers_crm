from django.urls import path
from dashboard import views as dashboard_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('dashboard',dashboard_views.dashboard),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
