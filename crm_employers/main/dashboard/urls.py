from django.urls import path
from dashboard.dashboard_operations.main import views as main_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # main dashboard operations
    path('record/create',main_views.CreateRecord.as_view(),name='add_record'),
    path('record/update',main_views.UpdateRecord.as_view(),name='update_record'),
    path('record/delete',main_views.DeleteRecord.as_view(),name='delete_position'),
    path('record/get',main_views.GetRecord.as_view(),name='get_record'),
    # path('record/position/update',main_views.SwitchPosition.as_view(),name='switch_position'),
    # path('record/position/compare',dashboard_views.CompareRecord.as_view(),name='compare_record'),
    # path('insights/update',dashboard_views.UpdateInsights.as_view(),name='update_insights'),
    # path('insights/get',dashboard_views.GetInsights.as_view(),name='get_insights'),
    # path('insights/add',dashboard_views.AddInsights.as_view(),name='add_insights'),
    # path('insights/delete',dashboard_views.DeleteInsights.as_view(),name='delete_insights'),

    # additional operations
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
