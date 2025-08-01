from django.urls import path
from . import api_views

app_name='userprofile'
urlpatterns=[
    path('',api_views.UserListCreateView.as_view, name='user-list-create'),
    path('<int:id>/details/')
]