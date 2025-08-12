from rest_framework.generics import GenericAPIView
from rest_framework import response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from rest_framework import status
from utils import choices as choices_
from . import serializers as serializers_
from . import models

from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, 
    RetrieveModelMixin, UpdateModelMixin, 
    DestroyModelMixin
    )

@api_view(['GET'])
@login_required
def get_season_choices(request):
    season_choices=[{"key": item.value, "label": item.label} for item in choices_.SeasonChoices]
    return response.Response(season_choices, status=status.HTTP_200_OK)

class ActivityTypeListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):
    permission_classes=[]
    serializer_class=serializers_.ActivityTypeSerializer
    queryset=models.ActivityType.objects.all()

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class ActivityTypeDetailUpdateDeleteView(
    GenericAPIView, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin
):
    permission_classes=[]
    serializer_class=serializers_.ActivityTypeSerializer
    queryset=models.ActivityType.objects.all()
    lookup_field='id'
    lookup_url_kwarg='id'

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

class ActivityListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):
    permission_classes=[]
    def get_serializer_class(self):
        if self.request.method=='GET':
            return serializers_.ActivityListSerializer
        return serializers_.ActivityCreateSerialzier
    queryset=models.Activity.objects.all()
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
class ActivityDetailUpdateDeleteView(
    GenericAPIView, RetrieveModelMixin, 
    UpdateModelMixin, DestroyModelMixin
):
    serializer_class=serializers_.ActivityCreateSerialzier
    lookup_field='id'
    lookup_url_kwarg='id'
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def put(self, request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

class DestinationListCreateView(GenericAPIView,ListModelMixin, CreateModelMixin):
    permission_classes=[]
    queryset=models.Destination.objects.all()
    def get_serializer_class(self):
        if self.request.method=='GET':
            return serializers_.DestinationListSerializer
        return serializers_.DestinationCreateSerialzier
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self, request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class DestinationDetailUpdateDeleteView(
    GenericAPIView, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin
):
    serializer_class=serializers_.DestinationCreateSerialzier
    lookup_field='id'
    lookup_url_kwarg='id'
    queryset=models.Destination.objects.all()

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)
    
class RouteListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):
    def get_serializer_class(self):
        if self.request.method=='GET':
            return serializers_.RouteListSerializer
        return serializers_.RouteCreateSerializer
    queryset=models.Route.objects.all()
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
class RouteDetailUpdateDeleteView(
    GenericAPIView, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin
):
    permission_classes=[]
    serializer_class=serializers_.RouteCreateSerializer
    queryset=models.Route.objects.all()
    lookup_field='id'
    lookup_url_kwarg='id'
    
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def patch(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

class TravelListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):
    permission_classes=[]
    def get_serializer_class(self):
        if self.request.method=='GET':
            return serializers_.TravelListSerializer
        return serializers_.TravelCreateSerializer
    queryset=models.Travel.objects.all()

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class TravelDetailUpdateDeleteView(
    GenericAPIView, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin
):
    permission_classes=[]
    serializer_class=serializers_.TravelCreateSerializer
    queryset=models.Travel.objects.all()
    lookup_field='id'
    lookup_url_kwarg='id'

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def patch(self, request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)    