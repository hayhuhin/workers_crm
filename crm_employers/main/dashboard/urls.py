from django.urls import path
from dashboard import views as dashboard_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('getRecord',dashboard_views.GetRecord.as_view(),name='get_record'),
    path('AddRecord',dashboard_views.AddRecord.as_view(),name='add_record'),
    path('UpdateRecord',dashboard_views.UpdateRecord.as_view(),name='update_record'),
    # path('edit_graph',dashboard_views.dashboard),
    # path('switch_graph',dashboard_views.dashboard),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
