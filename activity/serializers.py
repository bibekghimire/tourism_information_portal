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
        validated_data['last_modified_by']
        return super().update(instance,validated_data)

class CreateUpdateActivityTypeSerializer(BaseSerializer):
    class Meta:
        model=ActivityType
        fields=['title',]

class ActivityTypeListSerializer(serializers.ModelSerializer):
    url=serializers.SerializerMethodField()
    class Meta:
        model=ActivityType
        fields=['title','url','id']
    def get_url(self,obj):
        raise("define url method")
        request=self.context.get('request',None)
        if request:
            return reverse(
                '',
            )

class CreateActivitySerialzier(BaseSerializer):
    type=serializers.SlugRelatedField(queryset=ActivityType.objects.all(), slug_field='title')
    class Meta:
        model=Activity
        fields=['title','type','featured_photo']

class ActivityListSerializer(serializers.ModelSerializer):
    url=serializers.SerializerMethodField
    class Meta:
        model=Activity
        fields=['title','url','id']

class CreateDestinationSerialzier(BaseSerializer):
    class Meta:
        model=Destination
        fields=[
            'title','activity','geo_location','image1','image2','image3'
            'start_point','end_point'
        ]

class DestinationListSerializer(serializers.ModelSerializer):
    url=serializers.SerializerMethodField()
    class Meta:
        model=Destination
        fields=['title','url','id']

class CreateRouteSerializer(BaseSerializer):
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
        if request:
            return reverse(
                'view',
                request=request,
                kwargs=''
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
        kwargs={}
        if request:
            return reverse(
                'view_name',
                kwargs=kwargs,
                request=request
            )
