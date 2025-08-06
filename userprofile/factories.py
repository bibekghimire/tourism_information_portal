import factory
from faker import Faker
from django.contrib.auth import get_user_model
from userprofile.models import UserProfile
from utils import choices


User=get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=User
    
    username=factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall('set_password', 'testpass')

class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=UserProfile

    user=factory.SubFactory(UserFactory)
    first_name=factory.LazyAttribute(lambda x: Faker().name()[:20])
    phone_number = factory.Sequence(lambda n: f"98{str(10000000 + n).zfill(8)}")
    last_name=factory.LazyAttribute(lambda x: Faker().name()[:20])
    email = factory.Sequence(lambda n: f"email{n}@fact.com")
    date_of_birth="2000-01-01"
    role=factory.Iterator([choice.value for choice in choices.RoleChoices])



    