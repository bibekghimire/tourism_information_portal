from rest_framework import serializers
from .models import Visitor, Review, Group
from django.contrib.auth.models import User
from userprofile.models import UserProfile
from rest_framework.reverse import reverse
from activity.models import Route
from userprofile.serializers import ListUserProfileSerializer

#Group Serializer
class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields=['name']
    def create(self,validated_data):
        validated_data['created_by']=self.context.get('request').user.userprofile
        instance=super().create(validated_data)
        return instance

class GroupListSerializer(serializers.ModelSerializer):
    member_count=serializers.SerializerMethodField()
    url=serializers.SerializerMethodField()
    class Meta:
        model=Group
        fields=['name','url','member_count','id']
    def get_member_count(self,obj):
        return obj.members.count()
    def get_url(self,obj):
        request=self.context.get('request')
        kwargs={'id':obj.id}
        if request:
            return reverse(
                'visitor-record:group-retrieve-update',
                kwargs=kwargs,
                request=request
            )

class VisitorCreateSerializer(serializers.ModelSerializer):
    route=serializers.SlugRelatedField(queryset=Route.objects.all(),slug_field='name')
    class Meta:
        model=Visitor
        fields=['route','first_name','last_name','country',
                'address','contact_number','email','emergency_contact','age','group'
                ]

class VisitorListSerializer(serializers.ModelSerializer):
    url=serializers.SerializerMethodField()
    class Meta:
        model=Visitor
        fields=['full_name','contact_number','email','url']
    def get_url(self,obj):
        request=self.context.get('request')
        kwargs={'id':obj.id}
        if request:
            return reverse(
                'visitor-record:visitor-retrieve-update',
                kwargs=kwargs,
                request=request
            )

class GroupDetailSerializer(serializers.ModelSerializer):
    member_count=serializers.SerializerMethodField()
    members=VisitorListSerializer(many=True)
    created_by=ListUserProfileSerializer()
    class Meta:
        model=Group
        fields=['name','members','member_count','id',
                'created_at','last_modified','created_by','last_modified_by',
            ]
        read_only_fields=[
            'id',
            'created_at','last_modified','created_by','last_modified_by',
        ]
    def get_member_count(self,obj):
        return obj.members.count()

class VisitorDetailSerializer(serializers.ModelSerializer):
    group=GroupListSerializer()
    class Meta:
        model=Visitor
        fields = [
        'route', 'first_name', 'last_name', 'country', 'Address',
        'contact_number', 'email', 'emergency_contact', 'age', 'group',
        'created_at','last_modified','created_by','last_modified_by',
        ]