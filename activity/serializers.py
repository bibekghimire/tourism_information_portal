from rest_framework import serializers
from .models import Activity, ActivityType, Destination, Route, Travel
from django.contrib.auth import get_user_model

from userprofile.models import UserProfile
from rest_framework.reverse import reverse

class BaseSerializer(serializers.ModelSerializer):
    def create(self,validated_data):
        validated_data['created_by']=self.context.get('request').user
        return super().create(validated_data)
    def update(self,instance,validated_data):
        validated_data['last_modified_by']=self.context.get('request').user
        return super().update(instance,validated_data)

class ActivityTypeSerializer(BaseSerializer):
    class Meta:
        model=ActivityType
        fields=['title','id']
        read_only_fields=['id']

class ActivityCreateSerialzier(BaseSerializer):
    type=serializers.SlugRelatedField(queryset=ActivityType.objects.all(), slug_field='title')
    class Meta:
        model=Activity
        fields=['title','type','featured_photo']

class ActivityListSerializer(serializers.ModelSerializer):
    url=serializers.SerializerMethodField()
    class Meta:
        model=Activity
        fields=['title','url','id']
    def get_url(self,obj):
        request=self.context.get('request',None)
        kwargs={'id':obj.id}
        return reverse(
            'activity:activity-detail-update-delete',
            request=request,
            kwargs=kwargs,
        )

class DestinationCreateSerializer(BaseSerializer):
    activity=serializers.SlugRelatedField(
        many=True,
        queryset=Activity.objects.all(),
        slug_field='title'
    )
    class Meta:
        model=Destination
        fields=[
            'title','activity','geo_location','image1','image2','image3'
        ]

class DestinationListSerializer(serializers.ModelSerializer):
    url=serializers.SerializerMethodField()
    class Meta:
        model=Destination
        fields=['title','url','id']
    def get_url(self,obj):
        request=self.context.get('request',None)
        kwargs={'id':obj.id}
        return reverse(
            'activity:destination-detail-update-delete',
            request=request,
            kwargs=kwargs,
        )

class RouteCreateSerializer(BaseSerializer):
    destinations=serializers.SlugRelatedField(
        many=True,
        queryset=Destination.objects.all(),
        slug_field='title',
    )
    class Meta:
        model=Route
        fields=['title','destinations','start_point','end_point']

class RouteListSerializer(serializers.ModelSerializer):
    url=serializers.SerializerMethodField()
    class Meta:
        model=Route
        fields=['title','url']
    def get_url(self,obj):
        request=self.context.get('request',None)
        kwargs={'id':obj.id}
        if request:
            return reverse(
                'activity:route-detail-update-delete',
                request=request,
                kwargs=kwargs
            )

class TravelCreateSerializer(BaseSerializer):
    activities=serializers.SlugRelatedField(
        queryset=Activity.objects.all(),
        slug_field='title',
        many=True,
    )
    route=serializers.SlugRelatedField(
        queryset=Route.objects.all(),
        slug_field='title',
        many=True
    )
    class Meta:
        model=Travel
        fields=[
            'title','activities','route',
            'image1','image2','image3',
            'descriptions','duration',
            'difficulty',
            'max_altitude_m','min_altitude_m',
            'distance','best_season',
            'required_permits','is_guided_only',
        ]

class TravelListSerializer(serializers.ModelSerializer):
    url=serializers.SerializerMethodField()
    class Meta:
        model=Travel
        fields=['title','url']
    def get_ulr(self,obj):
        request=self.context.get('request')
        kwargs={'id':obj.id}
        if request:
            return reverse(
                'activity:travel-detail-update-delete',
                kwargs=kwargs,
                request=request
            )
