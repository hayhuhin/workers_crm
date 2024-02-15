from django.urls import path
from dashboard.dashboard_operations.main import views as main_views
from dashboard.dashboard_operations.additional import views as additional_views
from dashboard.insights import views as insight_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    #* main dashboard operations
    path('record/create',main_views.CreateRecord.as_view(),name='create_record'),
    path('record/update',main_views.UpdateRecord.as_view(),name='update_record'),
    path('record/delete',main_views.DeleteRecord.as_view(),name='delete_position'),
    path('record/get',main_views.GetRecord.as_view(),name='get_record'),

    #* additional dashboard operations
    path('record/switch',additional_views.SwitchRecord.as_view(),name='switch_record'),
    path('record/compare',additional_views.CompareRecord.as_view(),name='compare_record'),

    #* insights operations 
    path('insight/create',insight_view.CreateInsight.as_view(),name='create_insight'),
    path('insight/update',insight_view.UpdateInsight.as_view(),name='update_insight'),
    path('insight/delete',insight_view.DeleteInsight.as_view(),name='delete_insight'),
    path('insight/get',insight_view.GetInsight.as_view(),name='get_insight'),

    # additional operations
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
