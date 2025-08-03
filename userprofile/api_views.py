from rest_framework.generics import GenericAPIView
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

class UserListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):
    permission_classes=[IsAuthenticated]
    lookup_field='id'
    lookup_url_kwarg='id'
    def get_serializer_class(self):
        if self.request.method=='GET':
            return serializers_.UserListSerializer
        return serializers_.UserCreateSerializer
    def get_queryset(self):
        qs=User.objects.filter(is_superuser=False)
        return qs
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request,*args,**kwargs)
    
class UserRetrieveUpdateDeleteView(
    GenericAPIView,RetrieveModelMixin, DestroyModelMixin,
    UpdateModelMixin
):
    permission_classes=[IsAuthenticated]
    def get_serializer_class(self):
        if self.request.method=='PATCH':
            return serializers_.UserNameUpdateSerializer
        elif self.request.method=='GET':
            return serializers_.UserListSerializer
        else:
            return response("Method Not Allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    lookup_field='id'
    lookup_url_kwarg='id'
    queryset=User.objects.filter(is_superuser=False)
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def delete(self,request,*args,**kwargs):
        return self.delete(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)

class ChangePasswordView(GenericAPIView, UpdateModelMixin):
    permission_classes=[IsAuthenticated]
    serializer_class=serializers_.ChangePasswordSerializer
    queryset=User.objects.all()
    lookup_url_kwarg='id'
    lookup_field='id'
    def get_object(self):
        return self.request.user
    def patch(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)

class ResetPasswordView(GenericAPIView, UpdateModelMixin):
    permission_classes=[IsAuthenticated,IsAdminUser]
    serializer_class=serializers_.ResetPasswordSerializer
    queryset=User.objects.all()
    lookup_url_kwarg='id'
    lookup_field='id'
    def patch(self,request,*args,**kwargs):
        obj=self.get_object()
        assert(isinstance(obj,User))
        if request.user!=self.object:
            return self.patch(reqst,*args,**kwargs)
        return response("You Cannot Reset password yourself", status=status.HTTP_403_FORBIDDEN)


#User Profile View
class UserProfileListCreateView(GenericAPIView, CreateModelMixin, ListModelMixin):
    permission_classes=[IsAuthenticated]
    def get_serializer_class(self):
        if self.request.method=='POST':
            return serializers_.CreateUserProfileSerializer
        return serializers_.ListUserProfileSerializer
    def get_queryset(self):
        return models.UserProfile.all()
    lookup_field='id'
    lookup_url_kwarg='id'
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)  
    
    
class UserProfileDetailUpdateDeleteView(
    GenericAPIView, RetrieveModelMixin, UpdateModelMixin
):
    permission_classes=[IsAuthenticated]
    def get_serializer_class(self):
        return serializers_.DetailUserProfileSerializer
    def get_queryset(self):
        return models.UserProfile.objects.all()
    lookup_field='id'
    lookup_url_kwarg='id'
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request,*args,**kwargs)

    
class AdminDetailUserProfileView(
    GenericAPIView, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
):
    permission_classes=[IsAuthenticated]
    serializer_class=serializers_.AdminDetailUserProfileSerializer
    queryset=models.UserProfile.objects.all()
    lookup_field='id'
    lookup_url_kwarg='id'
    def get(self,request,*args,**kwargs):
        return self.retrieve(request, *args, **kwargs)
    def patch(self,request,*args, **kwargs):
        return self.partial_update(request,*args,**kwargs):
    def put(self,request, *args,**kwargs):
        return self.update(request, *args, **kwargs)
    def delete(self,request, *args, **kwargs):
        return self.destroy(request,*args,**kwargs)
    

