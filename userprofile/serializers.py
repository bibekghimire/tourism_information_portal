from .models import UserProfile
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth.password_validation import validate_password
from utils import validators
from rest_framework.validators import ValidationError
from utils import choices as choices_


#User Object Related Serializers
class UserListSerializer(serializers.ModelSerializer):
    '''To list All the users, with username and id '''
    class Meta:
        model=User
        fields=['username']
        read_only_fields=['username','id']

class UserCreateSerializer(serializers.ModelSerializer):
    password1=serializers.CharField(max_length=32,write_only=True, validators=[validators.password_validator])
    password2=serializers.CharField(max_length=32,write_only=True,)
    username=serializers.CharField(validators=[validators.username_validator])
    class Meta:
        model=User
        fields=['username','password1','password2']
    def validate(self,data):
        validators.match_password(data['password1'],data['password2'])
        username=data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError(f'User with username: {username} already exists')
        return data
    def create(self,validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1']
        )
        return user
    
class UserNameUpdateSerializer(serializers.ModelSerializer):
    username=serializers.CharField(validators=[validators.username_validator])
    class Meta:
        model=User
        fields=['username']
    def update(self,instance,validated_data):
        username=validated_data['username']
        if User.objects.exclude(instance.username).filter(username).exists():
            raise serializers.ValidationError(f'User with username: {username} already exists')
        setattr(instance,'username',validated_data['username'])
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password=serializers.CharField(max_length=32, write_only=True)
    password1=serializers.CharField(max_length=32,write_only=True, validators=[validators.password_validator])
    password2=serializers.CharField(max_length=32, write_only=True)
    class Meta:
        model=User
        fields=['username','old_password','password1','password2']
        read_only_fields=['username']
    
    def update(self,instance,validated_data):
        if instance.check_password(validated_data['old_password']):
            instance.set_password(validated_data['password1'])
        else:
            raise serializers.ValidationError("Old Password Incorrect")
    def create(self,validated_data):
        raise serializers.ValidationError("Create Method not allowed on Change Password")

class ResetPasswordSerializer(serializers.ModelSerializer):
    password1=serializers.CharField(max_length=32,write_only=True, validators=[validators.password_validator])
    password2=serializers.CharField(max_length=32, write_only=True)
    class Meta:
        model=User
        fields=['username', 'password1','password2']
        read_only_fields=['username']
    def validate(self,data):
        validators.match_password(data['password1'], data['password2'])
        return data
    def update(self,instance,validated_data):
        if isinstance(instance,User):
            instance.set_password(validated_data['password1'])
        else:
            raise serializers.ValidationError("Not a User Instance")
        return instance
    


#UserProfileRelatedSerializers
class ListUserProfileSerializer(serializers.ModelSerializer):
    url=serializers.SerializerMethodField()
    class Meta:
        model=UserProfile
        fields=['full_name', 'display name','phone_number', 'role','url']
    def get_url(self,obj):
        request=self.context.get['request', None]
        return reverse(
            '',
            kwargs='kwargs',
            request=request
        )

class CreateUserProfileSerializer(serializers.ModelSerializer):
    choices=serializers.ChoiceField(choices_.RoleChoices)
    class Meta:
        model=UserProfile
        fields=['first_name','last_name','display_name','email','phone_number','date_of_birth','user','profile_picture','status']



