from django.db import models
from django.contrib.auth.models import User
from utils import choices as choices_
from userprofile.models import UserProfile


class BaseModel(models.Model):
    '''provides fields commmon to all models
    provides save method and other common methods
    like Meta: ordering; author: returning full_name of creator
    '''
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
     '''
     Activity type would be Adventure and sports, Cultural
     "Academic and Research"
     '''
     title=models.CharField(max_length=100, help_text="Adventure and sports, Cultural", unique=True)

class Activity(BaseModel):
     """
     Activities would be based on ActivityType such as Trekking 
     for Adventure and sports
     recreation and spa for spiritural etc, can be changed on demand"""
     title=models.CharField(max_length=50,unique=True)
     type=models.ForeignKey(ActivityType, on_delete=models.PROTECT, related_name='activities')
     featured_photo=models.ImageField(null=True, blank=True)
     class Meta:
          ordering=['created_at']

class Destination(BaseModel):
    """The Destinations would be any destiny, that is physical location
    suppose: xyz_basecamp, xyz_view_point, xyz_model_farm
    """
    title=models.CharField(max_length=100, unique=True)
    activity=models.ManyToManyField(Activity, related_name='destinations')
    geo_location=models.CharField(max_length=100) #switch to Lat and long
    image1=models.ImageField(blank=True, null=True)
    image2=models.ImageField(blank=True, null=True)
    image3=models.ImageField(blank=True, null=True)

class Route(BaseModel):
     """
     These are specially for tracking purpose
     it has start and end point
     such as xyz_trekking route, xyz_research trip
     in near future checkpoints too. 
     """
     title=models.CharField(max_length=50, unique=True)
     destinations=models.ManyToManyField(Destination, related_name='routes',)
     start_point = models.CharField(max_length=100)
     end_point = models.CharField(max_length=100)

class Travel(BaseModel):
    """
    This is for tourism destinations like
    abc_trekking, avc_sports, abc_travell etc"""
    title=models.CharField("Activity Title",max_length=100,unique=True)
    activities=models.ForeignKey(Activity, related_name='travels', on_delete=models.SET_NULL, null=True)
    route=models.ManyToManyField(Route,verbose_name="Route",)
    image1=models.ImageField(blank=True, null=True)
    image2=models.ImageField(blank=True, null=True)
    image3=models.ImageField(blank=True, null=True)
    descriptions=models.TextField("Descriptions")
    duration=models.PositiveSmallIntegerField("Expected Duration in days")
    difficulty = models.CharField(
    choices=[('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Hard')],
    max_length=10
    )
    max_altitude_m = models.IntegerField(help_text="In meters")
    min_altitude_m = models.IntegerField(help_text="In meters", null=True, blank=True)
    distance = models.FloatField(null=True, blank=True,help_text="In K.meters")  # optional
    best_season = models.CharField(
    choices=choices_.SeasonChoices,
    max_length=20
    )
    required_permits = models.TextField(null=True, blank=True)  # or a separate Permit model
    is_guided_only = models.BooleanField(default=False)


