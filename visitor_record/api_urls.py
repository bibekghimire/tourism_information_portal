#api_urls.py
from django.urls import path
from . import api_views
#api/visitor/
app_name='visitor-record'
urlpatterns=[
    path('',api_views.VisitorListCreateView.as_view(), name='visitor-list-create'),
    path('<int:id>/',api_views.VisitorRetriveUpdateDeleteView.as_view(),
         name='visitor-retrieve-update'),
    path('group/',api_views.GroupListCreateView.as_view(), name='group-list-create'),
    path('group/<int:id>/', api_views.GroupRetriveUpdateDeleteView.as_view(),
         name='group-retrieve-update'),
]
