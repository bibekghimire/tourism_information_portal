import factory
from faker import Faker
from userprofile.factories import UserProfileFactory, UserFactory
import random
from activity.models import ActivityType, Activity, Destination, Route

def activity_title(n):
    r=n%10
    titles=[
        'Trekking', 'Camping', 'Hiking','cannonying','Zip Flyer',
        'research','educational','vacation','picnic','festival',
    ]
    return titles[r] if r>0 else titles[random.randint(0,9)]

class ActivityTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=ActivityType
    title=factory.Sequence(lambda n: f'activitytype{n}')
    created_by=factory.SubFactory(UserFactory)

class ActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Activity
    type=factory.SubFactory(ActivityTypeFactory)
    title=factory.Sequence(activity_title)

class DestinationFactory(factory.django.DjangoModelFactory):
    title=factory.Sequence(lambda n: f'destination{n}')
    activity=factory.SubFactory(ActivityFactory)
    geo_location='LAT LONG'
    start_point=factory.Sequence(lambda n: f'start{n}')
    end_point=factory.Sequence(lambda n: f'end{n}')

class RouteFactory(factory.django.DjangoModelFactory):