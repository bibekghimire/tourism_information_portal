from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from . import serializers as serializers_
from . import models
from django.contrib.auth.models import User
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, RetrieveModelMixin, 
    UpdateModelMixin, DestroyModelMixin
)
from rest_framework import response, status
from utils import permissions as permissions_
from utils import choices as choices_
from django.db.models import Q

ADMIN=choices_.RoleChoices.ADMIN
STAFF=choices_.RoleChoices.STAFF
CREATOR=choices_.RoleChoices.CREATOR

def userprofile_filter(self,qs):
    '''
    Helper function: returns filtered queryset to list UserProfiles.
    requested by `admin` all user profiles except admins
    requested by staff all creator list
    None for others
    '''
    condition1=Q(role=STAFF)
    condition2=Q(role=CREATOR)
    if self.request.user.is_authenticated:
        if self.request.user.is_superuser:
            return qs
        if self.request.user.role==ADMIN:
            return qs.filter(condition1 | condition2)
    return qs.filter(condition2)
def user_filter(self,qs):
    user=self.request.user
    if user.is_superuser:
        return qs
    elif user.role ==ADMIN:
        return qs.filter(
            Q(is_superuser=False) & 
            (Q(userprofile__isnull=False) & (Q(userprofile__role=STAFF) | Q(userprofile__role=CREATOR))) |
            (Q(userprofile__isnull=True))
        )    
    elif user.role==STAFF:
        return qs.filter(
             Q(is_superuser=False) & 
            (Q(userprofile__isnull=False) & (Q(userprofile__role=CREATOR))) |
            (Q(userprofile__isnull=True))
        )
    else:
        return qs.none()

class UserListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):
    '''The user lists are available only to STAFF and ADMIN'''
    permission_classes=[IsAuthenticated,permissions_.CanCreateUpdateUser ]
    lookup_field='id'
    lookup_url_kwarg='id'
    def get_serializer_class(self):
        if self.request.method=='GET':
            return serializers_.UserListSerializer
        return serializers_.UserCreateSerializer
    def get_queryset(self):
        queryset=User.objects.all()
        return user_filter(self,queryset)
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request,*args,**kwargs)
 
class SelfUserDetailView(GenericAPIView,RetrieveModelMixin):
    permission_classes=[IsAuthenticated]
    serializer_class=serializers_.SelfUserDetailSerializer
    def get_object(self):
        return self.request.user
    def get(self,request,*args,**kwargs):
        return self.retrieve(request, *args,**kwargs)   

class UserRetrieveUpdateDeleteView(
    GenericAPIView,RetrieveModelMixin, DestroyModelMixin,
    UpdateModelMixin
):
    '''
    superiro user can update the user details for the user 
    below it
    '''
    permission_classes=[IsAuthenticated, permissions_.CanCreateUpdateUser]
    def get_serializer_class(self):
        if self.request.method=='PATCH':
            return serializers_.UserUpdateSerializer
        elif self.request.method=='GET':
            return serializers_.UserListSerializer
        else:
            return response("Method Not Allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    lookup_field='id'
    lookup_url_kwarg='id'
    def get_queryset(self):
        qs=User.objects.all()
        return user_filter(self,qs)
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        target_object=self.get_object()
        if request.user==target_object:
            return response.Response("You Cannot Update yourself, Contact Developer Team", status=status.HTTP_403_FORBIDDEN)
        return self.partial_update(request,*args,**kwargs)

class ChangePasswordView(GenericAPIView, UpdateModelMixin):
    '''to change the password for self user'''
    permission_classes=[IsAuthenticated]
    serializer_class=serializers_.ChangePasswordSerializer
    def get_object(self):
        return self.request.user
    def patch(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)

class ResetPasswordView(GenericAPIView, UpdateModelMixin):
    '''To reset the password for the user lower in rank '''
    permission_classes=[IsAuthenticated,permissions_.CanCreateUpdateUser]
    serializer_class=serializers_.ResetPasswordSerializer
    def get_queryset(self):
        queryset=User.objects.all()
        return user_filter(self,queryset)
    lookup_url_kwarg='id'
    lookup_field='id'
    def patch(self,request,*args,**kwargs):
        obj=self.get_object()
        assert(isinstance(obj,User))
        if request.user != obj:
            return self.partial_update(request,*args,**kwargs)
        return response("You Cannot Reset password yourself", status=status.HTTP_403_FORBIDDEN)

#User Profile View
class UserProfileListCreateView(GenericAPIView, CreateModelMixin, ListModelMixin):
    '''
    only staffs and admin can create and view userprofiles
    '''
    permission_classes=[IsAuthenticated, permissions_.CanCreateUpdateUser]
    def get_serializer_class(self):
        if self.request.method=='POST':
            return serializers_.CreateUserProfileSerializer
        return serializers_.ListUserProfileSerializer
    def get_queryset(self):
        #apply filter if required to filter out userlist for different users
        qs=models.UserProfile.objects.all()
        return userprofile_filter(self,qs)
    lookup_field='id'
    lookup_url_kwarg='id'
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)  
  
class SelfUserProfileDetailUpdateView(
    GenericAPIView, RetrieveModelMixin, UpdateModelMixin
):
    _name='self'
    '''Authenitcated Users can access this view
    retrieves/updates self.request.user.userprofile
    '''
    permission_classes=[IsAuthenticated]
    serializer_class=serializers_.SelfDetailUserProfileSerializer

    def get_object(self):
        profile= getattr(self.request.user,'userprofile', None) 
        if profile:
            return profile
        else:
            return response.Response("UserProfile Not Found", status=status.HTTP_404_NOT_FOUND)
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def put(self, request, *args, **kwargs):
        return self.update(request,*args,**kwargs)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request,*args,**kwargs)

class SuperUserProfileDetailUpdateDeleteView(
    GenericAPIView, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
):
    '''
    User in higher rank can access this view and 
    update some deatils that ar not available to update for self view'''
    permission_classes=[IsAuthenticated,permissions_.CanCreateUpdateUser]
    serializer_class=serializers_.SuperDetailUserProfileSerializer

    def get_queryset(self):
        queryset=models.UserProfile.objects.all()
        return userprofile_filter(self,queryset)
        
    lookup_field='id'
    lookup_url_kwarg='id'

    def get(self,request,*args,**kwargs):
        return self.retrieve(request, *args, **kwargs)
    def patch(self,request,*args, **kwargs):
        return self.partial_update(request,*args,**kwargs)
    def put(self,request, *args,**kwargs):
        return self.update(request, *args, **kwargs)
    def delete(self,request, *args, **kwargs):
        return self.destroy(request,*args,**kwargs)

class GetRoleChoices(APIView):
    '''Returns role choices to select in format {
                    'value':choice.value,
                    'label':choice.label,
                }
    to assign a role in Userprofile Creation
    '''
    permission_classes=[IsAuthenticated, permissions_.CanCreateUpdateUser]
    def get(self, request,*args,**kwargs):
        if request.user.is_superuser:
            role_choices=[
                {
                    'value':choice.value,
                    'label':choice.label,
                }
                for choice in choices_.RoleChoices
            ]
            return response.Response(role_choices)
        user_role = getattr(request.user, "role", None)
        return response.Response(choices_.RoleChoices.get_assignable_roles(user_role))

class GetUsers(GenericAPIView, ListModelMixin):
    '''
    returns list of users that are created by the requested user and 
    are not associated with any userprofile Yet
    '''
    permission_classes=[IsAuthenticated, permissions_.CanCreateUpdateUser]
    serializer_class=serializers_.UserNameSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.filter(userprofile__isnull=True)
        qs=User.objects.filter(
            Q(is_superuser=False) &
            (Q(userprofile__isnull=True) & Q(extension__created_by=self.request.user))
        )
        
        return qs
    def get(self, request,*args,**kwargs):
        return self.list(request,*args,**kwargs)