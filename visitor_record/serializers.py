from rest_framework import serializers
from .models import Visitor, Review, Group
from django.contrib.auth.models import User
from userprofile.models import UserProfile


#Group Serializer
class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields=['name']
    def create(self,validated_data):
        validated_data['creted_by']=self.context.get('request').user.userprofile
        super().create(validated_data)

class GroupListSerializer(serializers.ModelSerializer):
    member_count=serializers.SerializerMethodField()
    url=serializers.SerializerMethodField()
    class Meta:
        model=Group
        fields=['name','url','member_count']
    def get_member_count(self,obj):
        return obj.members.count()

class VisitorCreateSerializer(serializers.ModelSerializer):
    route=serializers.SlugRelatedField()
    class Meta:
        model=Visitor
        fields=['route','first_name','last_name','country',
                'address','contact_number','email','emergency_contact','age','group'
                ]

class VisitorListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Visitor
        fields=['full_name','contact_number','email',]

class GroupDetailSerializer(serializers.ModelSerializer):
    member_count=serializers.SerializerMethodField()
    members=VisitorListSerializer()
    class Meta:
        model=Group
        fields=['name','members','member_count','id']

class VisitorDetailSerializer(serializers.ModelSerializer):
    group=GroupListSerializer()
    class Meta:
        model=Visitor
        fields = [
        'route', 'first_name', 'last_name', 'country', 'Address',
        'contact_number', 'email', 'emergency_contact', 'age', 'group',
        'created_at','last_modified','created_by','last_modified_by',
        ]