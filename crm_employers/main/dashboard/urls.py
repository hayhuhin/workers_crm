from django.urls import path
from dashboard import views as dashboard_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('GetRecord',dashboard_views.GetRecord.as_view(),name='get_record'),
    path('AddRecord',dashboard_views.AddRecord.as_view(),name='add_record'),
    path('UpdateRecord',dashboard_views.UpdateRecord.as_view(),name='update_record'),
    path('SwitchPosition',dashboard_views.SwitchPosition.as_view(),name='switch_position'),
    path('DeleteRecord',dashboard_views.DeleteRecord.as_view(),name='delete_position'),
    path('CompareRecord',dashboard_views.CompareRecord.as_view(),name='compare_record'),
    path('UpdateInsights',dashboard_views.UpdateInsights.as_view(),name='update_insights'),
    path('AddInsights',dashboard_views.AddInsights.as_view(),name='add_insights'),
    path('GetInsights',dashboard_views.GetInsights.as_view(),name='get_insights'),
    path('DeleteInsights',dashboard_views.DeleteInsights.as_view(),name='delete_insights'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
