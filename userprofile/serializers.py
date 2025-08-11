from .models import UserProfile, UserExtension
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth.password_validation import validate_password
from utils import validators
from rest_framework.validators import ValidationError
from utils import choices as choices_
from utils import permissions as permissions_

ADMIN=choices_.RoleChoices.ADMIN
STAFF=choices_.RoleChoices.STAFF
CREATOR=choices_.RoleChoices.CREATOR


#User Object Related Serializers
class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username']

class SelfUserDetailSerializer(serializers.ModelSerializer):
    profile_url=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=['username','role','profile_url']
        read_only_fields=['username','url','profile_url']
    def get_profile_url(self,object):
        request=self.context.get('request',None)
        userprofile=getattr(object,'userprofile',None)
        if request:
            if userprofile:
                return reverse(
                    'userprofile:self-profile-detail-update',
                    request=request,
                )
        return None

class UserListSerializer(serializers.ModelSerializer):
    '''To list All the users, with username and id '''
    url=serializers.SerializerMethodField()
    profile_url=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=['username','id','url','role','profile_url']
        read_only_fields=['username','id','url','role','profile_url']
    def get_url(self,object):
        request=self.context.get('request',None)
        if request:
            kwargs={'id':object.id}
            return reverse(
                'userprofile:user-retrieve-update-delete',
                kwargs=kwargs,
                request=request,
            )
    def get_profile_url(self,object):
        request=self.context.get('request',None)
        userprofile=getattr(object,'userprofile',None)
        if userprofile:
            kwargs={
                'id':userprofile.id
            }
            if request:
                if userprofile:
                    return reverse(
                        'userprofile:super-userprofile-detail-update-delete',
                        request=request,
                        kwargs=kwargs,
                    )
        return None

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
        user.save()
        UserExtension.objects.create(user=user, created_by=self.context.get('request').user)
        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    username=serializers.CharField(validators=[validators.username_validator])
    is_active=serializers.BooleanField()
    class Meta:
        model=User
        fields=['username','is_active']
    def update(self,instance,validated_data):
        username=validated_data['username']
        is_active=validated_data['is_active']
        if User.objects.exclude(id=instance.id).filter(username=username).exists():
            raise serializers.ValidationError(f'User with username: {username} already exists')
        setattr(instance,'username',validated_data['username'])
        setattr(instance,'is_active',is_active)
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
    
    def validate(self,data):
        if validators.match_password(data['password1'],data['password2']):
            return data
        else:
            raise serializers.ValidationError("Both Password Must Match")
    def update(self,instance,validated_data):
        if instance.check_password(validated_data['old_password']):
            instance.set_password(validated_data['password1'])
            instance.save()
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
            instance.save()
        else:
            raise serializers.ValidationError("Not a User Instance")
        return instance

#UserProfileRelatedSerializers

class ListUserProfileSerializer(serializers.ModelSerializer):
    url=serializers.SerializerMethodField()
    class Meta:
        model=UserProfile
        fields=['full_name', 'display_name','phone_number','url','role']
    def get_url(self,obj):
        request=self.context.get('request', None)
        kwargs={
            'id':obj.id
        }
        return reverse(
            'userprofile:super-userprofile-detail-update-delete',
            kwargs=kwargs,
            request=request
        )

class CreateUserProfileSerializer(serializers.ModelSerializer):
    # choices=serializers.ChoiceField(choices_.RoleChoices)
    user=serializers.SlugRelatedField(queryset= User.objects.filter(userprofile__isnull=True),slug_field='username' )

    class Meta:
        model=UserProfile
        fields=['first_name','last_name',
                'display_name','email','phone_number',
                'date_of_birth',
                'user','role',
                'profile_picture']
    def validate_user(self, user):
        if self.context.get('request').user.role !=ADMIN or not self.context.get('request').user.is_superuser :
            if user.extension.created_by != self.context.get('request').user:
                raise serializers.ValidationError(
                f'This user: {user.username} is not allowed to {self.context.get('request').user.username} to assign'
            )
        if hasattr(user,'userprofile'):
            raise serializers.ValidationError(
                f'This user: {user.username} already associated with profile: {user.userprofile.full_name}'
            )
        return user

    def create(self,validated_data):
        user=self.context.get('request').user
        assigned_role=validated_data['role']
        if user.role==ADMIN and assigned_role==ADMIN:
            raise serializers.ValidationError("Role Assignment Not allowed")
        elif user.role==STAFF and assigned_role in [ADMIN,STAFF]:
            raise serializers.ValidationError(f"Role: {assigned_role} Assignment Not allowed to {user.role}")
        elif user.role==CREATOR:
            raise serializers.ValidationError("Role Assignment Not allowed")
        else:
            validated_data['created_by']=user
            profile=UserProfile.objects.create(**validated_data)
            profile._validated=True
            profile.save()
            return profile
    def update(self,instance,validate_data):
        raise serializers.ValidationError("Method Not Allowed")

class SelfDetailUserProfileSerializer(serializers.ModelSerializer):
    user=SelfUserDetailSerializer() #change to UserNameSerialzier
    class Meta:
        model=UserProfile
        fields=[
            'first_name', 'last_name', 'display_name',
            'email', 'phone_number', 'date_of_birth',
            'user', 'role','profile_picture',
            'created_by', 'created_at',
            'last_modified','modified_by'
        ]   
        read_only_fields=[
            'email', 'phone_number',
            'user','role',
            'created_by', 'created_at',
            'last_modified','modified_by',

        ]

class SuperDetailUserProfileSerializer(serializers.ModelSerializer):
    user=serializers.SlugRelatedField(queryset= User.objects.all(),slug_field='username')
    class Meta:
        model=UserProfile
        fields=[
            'first_name', 'last_name', 'display_name',
            'email', 'phone_number', 'date_of_birth',
            'user','role', 'profile_picture',
            'created_by', 'created_at',
            'last_modified','modified_by',
        ]
        read_only_fields=['created_by', 'created_at',
                          'last_modified','modified_by',
                          ]

    def update(self,instance,validated_data):
        user=self.context.get('request').user
        assigned_role=validated_data.get('role',None)
        if assigned_role:
            if user.role==ADMIN and assigned_role==ADMIN:
                raise serializers.ValidationError("Role Assignment Not allowed")
            elif user.role==STAFF and assigned_role in [ADMIN,STAFF]:
                raise serializers.ValidationError("Role Assignment Not allowed")
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance
