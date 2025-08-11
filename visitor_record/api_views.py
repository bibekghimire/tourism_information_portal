#api_views.py
from . models import  Visitor, Review, Group
from . import serializers as serializers_
from rest_framework.permissions import IsAuthenticated
from userprofile.models import UserProfile

from rest_framework.generics import GenericAPIView
from rest_framework import mixins

class GroupListCreateView(GenericAPIView, 
                          mixins.ListModelMixin, 
                          mixins.CreateModelMixin
                          ):
    permission_classes=[IsAuthenticated]
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
    
class GroupRetriveUpdateDeleteView(
    GenericAPIView, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    serializer_class=serializers_.GroupDetailSerializer
    queryset=Group.objects.all()
    lookup_field='id'
    lookup_url_kwarg='id'
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

class VisitorListCreateView(GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    def get_serializer_class(self):
        if self.request.method=='POST':
            return serializers_.VisitorCreateSerializer
        return serializers_.VisitorListSerializer
    queryset=Visitor.objects.all()
    lookup_field='id'
    lookup_url_kwarg='id'
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
class VisitorRetriveUpdateDeleteView(
    GenericAPIView, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    queryset=Visitor.objects.all()
    serializer_class=serializers_.VisitorDetailSerializer
    lookup_field='id'
    lookup_url_kwarg='id'
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
