import factory
from faker import Faker
from userprofile.factories import UserProfileFactory, UserFactory
import random
from activity.models import ActivityType, Activity, Destination, Route, Travel
from utils import choices

def activity_title(n):
    return f'activity {n}'
    r=n%10
    titles=[
        'Trekking', 'Camping', 'Hiking','cannonying','Zip Flyer',
        'research','educational','vacation','picnic','festival',
    ]
    return titles[r] if r>0 else titles[random.randint(0,9)]
class BaseFactory(factory.django.DjangoModelFactory):
    created_by=factory.SubFactory(UserFactory)
    class Meta:
        abstract=True

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
    start_point=factory.Sequence(lambda n: f'start{n}')
    end_point=factory.Sequence(lambda n: f'end{n}')
    @factory.post_generation
    def destinations(self,create,extracted,**kwargs):
        if not create:
            return 
        if extracted:
            self.destinations.set(extracted)
        else:
            self.destinations.set(DestinationFactory.create_batch(2))

class TravelFactory(BaseFactory):
    
    class Meta:
        model=Travel
    title=factory.Sequence(lambda n: f'travel{n}')
    descriptions=factory.Sequence(lambda n: f'Description {n}')
    difficulty=factory.LazyFunction(lambda : random.choice(['easy','moderate','hard']))
    duration=factory.LazyFunction(lambda : random.randint(1,15))
    max_altitude=factory.LazyFunction(lambda : random.randint(1000,5500))
    min_altitude=700
    distance=factory.LazyFunction(lambda : random.randint(1,55))
    best_season=factory.LazyFunction(lambda : random.choice([choice.value for choice in choices.SeasonChoices]))
    required_permits="No permits Required"
    is_guided_only=random.choice([True, False])
    
    @factory.post_generation
    def destinations(self,create,extracted,**kwargs):
        if not create:
            return 
        if extracted:
            self.destinations.set(extracted)
        else:
            self.destinations.set(DestinationFactory.create_batch(2))
    @factory.post_generation
    def activities(self,create,extracted,**kwargs):
        if not create:
            return 
        if extracted:
            self.activities.set(extracted)
        else:
            self.activities.set(ActivityFactory.create_batch(2))
    @factory.post_generation
    def routes(self,create,extracted,**kwargs):
        if not create:
            return 
        if extracted:
            self.routes.set(extracted)
        else:
            self.routes.set(RouteFactory.create_batch(2))
        