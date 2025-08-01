from django.db import models
from django.contrib.auth.models import User
from userprofile.models import UserProfile
from django.core.validators import MaxValueValidator

# Create your models here.

class BaseModel(models.Model):
    created_at=models.DateTimeField("Created At",auto_now_add=True)
    last_modified=models.DateTimeField("Last Updated", auto_now=True)
    created_by=models.ForeignKey(UserProfile, verbose_name="Created By", on_delete=models.PROTECT, related_name="%(class)s_added")
    _validated=False
    class Meta:
        abstract=True
        ordering=['last_modified']
    def save(self, *args, **kwargs):
        if not self._validated:
            self.full_clean()
        super().save(*args,**kwargs)
    @property
    def author(self):
        return self.created_by.full_name()

class Group(BaseModel):
    name=models.CharField("Group Name", max_length=100, unique=True)

class Visitor(BaseModel):
    first_name=models.CharField(verbose_name="First Name", max_length=100)
    last_name=models.CharField(verbose_name="Last Name", max_length=100)
    country=models.CharField(verbose_name="Country", max_length=100)
    Address=models.CharField(verbose_name="Address", max_length=100, blank=True)
    contact_number=models.CharField("Contact Number", max_length=20)
    email=models.EmailField(blank=True)
    emergency_contact=models.CharField("Emergency Contact", max_length=100)
    age=models.PositiveBigIntegerField("Age",validators=[MaxValueValidator(120)], blank=True)
    group=models.ForeignKey(Group, related_name='members', on_delete=models.PROTECT)

class Review(models.Model):
    reviewer=models.ForeignKey(Visitor, verbose_name="Review ", on_delete=models.PROTECT, related_name='reviews')
    content=models.TextField("Review Content")

