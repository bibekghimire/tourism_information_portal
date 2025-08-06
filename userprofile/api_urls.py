from django.urls import path
from . import api_views

app_name='userprofile'
'''/api/user/'''
urlpatterns=[
    path('',
         api_views.UserListCreateView.as_view(), 
         name='user-list-create'),
    path('<int:id>/details/',
         api_views.UserRetrieveUpdateDeleteView.as_view(),
         name='user-retrieve-update-delete'),
    path(
        'change-password/',
        api_views.ChangePasswordView.as_view(),
        name='user-change-password'
    ),
    path(
        'admin/<int:id>/reset-password/', 
        api_views.ResetPasswordView.as_view(),
        name='user-reset-password',
    ),
    path(
        'userprofile/', 
        api_views.UserProfileListCreateView.as_view(),
        name='userprofile-list-create'
    ),
    path('userprofile/details/', 
        api_views.SelfUserProfileDetailUpdateView.as_view(), 
        name='self-profile-update-delete'),
    path('admin/userprofile/<int:id>/details/',
         api_views.SuperUserProfileDetailUpdateDeleteView.as_view(),
         name='super-userprofile-detail-update-delete'),
    path('role-choices/',api_views.GetRoleChoices.as_view(),name='get-role-choices')
]