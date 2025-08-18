from django.urls import path
from . import api_views

'''
/api/activity/'''
app_name='activity'
urlpatterns=[
    path('type/',api_views.ActivityTypeListCreateView.as_view(),
         name='activity-type-list-create'),
    path('type/<int:id>/',api_views.ActivityTypeDetailUpdateDeleteView.as_view(),
         name='activity-type-detail-update-delete'),
    path('activities/',api_views.ActivityListCreateView.as_view(),
         name='activiy-list-create'),
    path('activities/<int:id>',api_views.ActivityDetailUpdateDeleteView.as_view(),
         name='activity-detail-update-delete'),
    path('destination/',api_views.DestinationListCreateView.as_view(),
         name='destination-list-create'),
    path('destination/<int:id>',api_views.DestinationDetailUpdateDeleteView.as_view(),
         name='destination-detail-update-delete'),
    path('route/',api_views.RouteListCreateView.as_view(),
         name='route-list-create'),
    path('route/<int:id>',api_views.RouteDetailUpdateDeleteView.as_view(),
         name='route-detail-update-delete'),
    path('travel/',api_views.TravelListCreateView.as_view(),
         name='travel-list-create'),
    path('travel/<int:id>',api_views.TravelDetailUpdateDeleteView.as_view(),
         name='travel-detail-update-delete'),
]
