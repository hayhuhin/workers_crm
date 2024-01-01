from django.urls import path
from dashboard import views as dashboard_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('record/get',dashboard_views.GetRecord.as_view(),name='get_record'),
    path('record/add',dashboard_views.AddRecord.as_view(),name='add_record'),
    path('record/update',dashboard_views.UpdateRecord.as_view(),name='update_record'),
    path('record/position/update',dashboard_views.SwitchPosition.as_view(),name='switch_position'),
    path('record/position/compare',dashboard_views.CompareRecord.as_view(),name='compare_record'),
    path('record/delete',dashboard_views.DeleteRecord.as_view(),name='delete_position'),
    path('insights/update',dashboard_views.UpdateInsights.as_view(),name='update_insights'),
    path('insights/get',dashboard_views.GetInsights.as_view(),name='get_insights'),
    path('insights/add',dashboard_views.AddInsights.as_view(),name='add_insights'),
    path('insights/delete',dashboard_views.DeleteInsights.as_view(),name='delete_insights'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
