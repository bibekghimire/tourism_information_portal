from django.db import models
from django.contrib.auth.models import User
from utils import choices as choices_
from userprofile.models import UserProfile
# Create your models here.

class BaseModel(models.Model):
    created_at=models.DateTimeField("Created At",auto_now_add=True)
    last_modified=models.DateTimeField("Last Updated", auto_now=True)
    created_by=models.ForeignKey(User, verbose_name="Created By", on_delete=models.PROTECT, related_name="%(class)s_added")
    _validated=False
    last_modified_by=models.ForeignKey(User, on_delete=models.PROTECT, related_name="%(class)s_modified", blank=True, null=True)
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
    
class ActivityType(BaseModel):
     title=models.CharField(max_length=10, help_text="Adventure and sports, Cultural")

class Activity(BaseModel):
     title=models.CharField(max_length=50,help_text="Trekking, Camping, Hiking, recreation")
     type=models.ForeignKey(ActivityType, on_delete=models.PROTECT, related_name='activities')
     fetured_photo=models.ImageField(null=True)
     class Meta:
          ordering=['created_at']

class Destination(BaseModel):
    title=models.CharField(max_length=100)
    activity=models.ManyToManyField(Activity, related_name='destinations')
    geo_loaction=models.CharField(max_length=100) #switch to Lat and long
    image1=models.ImageField(blank=True, null=True)
    image2=models.ImageField(blank=True, null=True)
    image3=models.ImageField(blank=True, null=True)
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)

class Route(BaseModel):
     title=models.CharField(max_length=50)
     destinations=models.ManyToManyField(Destination, related_name='routes', null=True)

class Travel(BaseModel):
    title=models.CharField("Activity Title",max_length=100,unique=True)
    activities=models.ForeignKey(Activity, related_name='travels', on_delete=models.SET_NULL, null=True)
    route=models.ManyToManyField(Route,null=True,verbose_name="Route",)
    image1=models.ImageField(blank=True, null=True)
    image2=models.ImageField(blank=True, null=True)
    image3=models.ImageField(blank=True, null=True)
    descriptions=models.TextField("Descriptions")
    duration=models.PositiveSmallIntegerField("Expected Duration")
    difficulty = models.CharField(
    choices=[('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Hard')],
    max_length=10
    )
    max_altitude_m = models.IntegerField(help_text="In meters")
    min_altitude_m = models.IntegerField(help_text="In meters", null=True, blank=True)
    distance_km = models.FloatField(null=True, blank=True)  # optional
    best_season = models.CharField(
    choices=[
        ('spring', 'Spring (Mar-May)'),
        ('summer', 'Summer (Jun-Aug)'),
        ('autumn', 'Autumn (Sep-Nov)'),
        ('winter', 'Winter (Dec-Feb)'),
        ('year_round', 'Year Round')
    ],
    max_length=20
    )
    activity_type=models.CharField(
        choices=[
             ('trekking',"Trekking"),

        ]
    )
    required_permits = models.TextField(null=True, blank=True)  # or a separate Permit model
    is_guided_only = models.BooleanField(default=False)


