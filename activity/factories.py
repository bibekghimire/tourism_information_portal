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
class BaseFactory(factory.django.DjangoModelFactory):
    created_by=factory.SubFactory(UserFactory)

class ActivityTypeFactory(BaseFactory):
    class Meta:
        model=ActivityType
    title=factory.Sequence(lambda n: f'activitytype{n}')
    

class ActivityFactory(BaseFactory):
    class Meta:
        model=Activity
    type=factory.SubFactory(ActivityTypeFactory)
    title=factory.Sequence(activity_title)

class DestinationFactory(BaseFactory):
    class Meta:
        model=Destination
    title=factory.Sequence(lambda n: f'destination{n}')
    # activity=factory.SubFactory(ActivityFactory)
    geo_location='LAT LONG'
    @factory.post_generation
    def activity(self,create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.activity.set(extracted)
        else:
            self.activity.set(ActivityFactory.create_batch(2))

class RouteFactory(BaseFactory):
    class Meta:
        model=Route
    title=factory.Sequence(lambda n: f'route{n}')
    start_point=title=factory.Sequence(lambda n: f'start{n}')
    end_point=title=factory.Sequence(lambda n: f'end{n}')
    @factory.post_generation
    def destinations(self,create,extracted,**kwargs):
        if not create:
            return 
        if extracted:
            self.destinations.set(extracted)
        else:
            self.destinations.set(DestinationFactory.create_batch(2))
