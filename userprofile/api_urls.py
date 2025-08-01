from django.urls import path
from . import api_views

app_name='userprofile'
urlpatterns=[
    path('',api_views.UserListCreateView.as_view(), name='user-list-create'),
    path('<int:id>/details/',api_views.UserRetrieveUpdateDeleteView.as_view(),name='user-retrieve-update-delete'),
    path(
        'change-password/',api_views.ChangePasswordView.as_view(),
        name='user-change-password'
    ),
    path(
        '<int:id>/reset-password/', api_views.ResetPasswordView.as_view(),
        name='user-reset-password',
    ),
]