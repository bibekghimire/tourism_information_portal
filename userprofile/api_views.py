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
from utils import choices

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
        qs=User.objects.all()
        return qs
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request,*args,**kwargs)
    
class UserRetrieveUpdateDeleteView(
    GenericAPIView,RetrieveModelMixin, DestroyModelMixin,
    UpdateModelMixin
):
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
    queryset=User.objects.filter()
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    # def delete(self,request,*args,**kwargs):
    #     return self.delete(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        target_object=self.get_object()
        if request.user==target_object:
            return response.Response("You Cannot Update yourself, Contact Developer Team", status=status.HTTP_403_FORBIDDEN)
        return self.partial_update(request,*args,**kwargs)

class ChangePasswordView(GenericAPIView, UpdateModelMixin):
    permission_classes=[IsAuthenticated]
    serializer_class=serializers_.ChangePasswordSerializer
    def get_object(self):
        return self.request.user
    def patch(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)

class ResetPasswordView(GenericAPIView, UpdateModelMixin):
    permission_classes=[IsAuthenticated,permissions_.CanCreateUpdateUser]
    serializer_class=serializers_.ResetPasswordSerializer
    queryset=User.objects.all()
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
        return models.UserProfile.objects.all()
    lookup_field='id'
    lookup_url_kwarg='id'
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)  
  
class SelfUserProfileDetailUpdateView(
    GenericAPIView, RetrieveModelMixin, UpdateModelMixin
):
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
    permission_classes=[IsAuthenticated,permissions_.CanCreateUpdateUser]
    serializer_class=serializers_.SuperDetailUserProfileSerializer

    queryset=models.UserProfile.objects.all()
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
    permission_classes=[IsAuthenticated, permissions_.CanCreateUpdateUser]
    def get(self, request,*args,**kwargs):
        if request.user.is_superuser:
            role_choices=[
                {
                    'value':choice.value,
                    'label':choice.label,
                }
                for choice in choices.RoleChoices
            ]
            return response.Response(role_choices)
        user_role = getattr(request.user, "role", None)
        return response.Response(choices.RoleChoices.get_assignable_roles(user_role))


    