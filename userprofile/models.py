from django.db import models
from utils import validators, choices
import os
from django.contrib.auth.models import User
import uuid
# Create your models here.

def get_user_role(self):
    if hasattr(self,'userprofile'):
        return self.userprofile.role
    return None
User.add_to_class('role',property(get_user_role))
def user_directory_path(instance, filename):
    ext=os.path.splitext(filename)[1] 
    return f'user_{instance.user.id}_{instance.first_name}/profile{ext}'

#############################################################################
class UserExtension(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='extension')
    created_by=models.ForeignKey(User,null=True, on_delete=models.SET_NULL, related_name='created_users')

    def __str__(self):
        return f"Extension of user: {self.user.usernmae}"

class CleanValidatedModel(models.Model):
    '''
    Base model that intelligently skips full_clean()
    if the instance was already validated (e.g., via a serializer).
    '''
    _validated = False  # Internal flag for validated instances
    created_at=models.DateTimeField("Created At",auto_now_add=True)
    class Meta:
        abstract=True

    def save(self, *args, **kwargs):
            # Only call full_clean if validation hasn’t run yet
            if not self._validated:
                print("validating invalidated data")
                self.full_clean()
            super().save(*args, **kwargs)

class UserProfile(CleanValidatedModel):
    first_name=models.CharField(
        "First Name", max_length=32,
        validators=[validators.no_whitespace,validators.name_validator]
    )
    
    last_name=models.CharField(
        "Last Name", max_length=32,
        validators=[validators.no_whitespace,validators.name_validator],
    )
    
    display_name=models.CharField(
        "Display Name", max_length=65, null=True, blank=True,
        validators=[validators.no_whitespace,validators.name_validator],
    )
    
    email=models.EmailField(unique=True,validators=[validators.no_whitespace,])
    
    phone_number=models.CharField(
        "Phone Number",unique=True, max_length=10,
        validators=[validators.no_whitespace,validators.phone_number_validator],
    )
    
    date_of_birth=models.DateField("Date of Birth",validators=[validators.age_validator])
    
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    
    profile_picture=models.ImageField(
        "Profile Picture", blank=True,
        upload_to=user_directory_path,
        validators=[validators.profile_picture_validator],
    )
    
    role=models.CharField(
        "User Roles",
        null=True,
        max_length=2,
        choices=choices.RoleChoices.choices,
    )
    
    status=models.CharField(
        "Status",
        null=True, max_length=3,
        choices=choices.StatusChoices.choices,
    )
    
    public_id=models.UUIDField("Public ID", default=uuid.uuid4, editable=False,unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}: {self.role}, {self.id}: {self.user.username}'
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        try:
            old=UserProfile.objects.get(pk=self.pk)
            if old.profile_picture and old.profile_picture != self.profile_picture:
                if os.path.isfile(old.profile_picture.path):
                    os.remove(old.profile_picture.path)
        except UserProfile.DoesNotExist:
            pass
        if not self.display_name.strip():
            self.display_name=self.get_full_name()
        super().save(*args,**kwargs)