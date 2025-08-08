#api_views.py
from . models import  Visitor, Review, Group
from . import serializers as serializers_

from userprofile.models import UserProfile

from rest_framework.generics import GenericAPIView
from rest_framework import mixins

class GroupListCreateView(GenericAPIView, 
                          mixins.ListModelMixin, 
                          mixins.CreateModelMixin
                          ):
    def get_serializer_class(self):
        if self.request.method=='POST':
            return serializers_.GroupCreateSerializer
        return serializers_.GroupListSerializer
    
    def get_queryset(self):
        return Group.objects.all()
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
class 