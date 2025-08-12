import factory
from faker import Faker
from django.contrib.auth import get_user_model
from visitor_record.models import Group, Visitor
from userprofile.factories import UserFactory

User=get_user_model()

class BaseFactory(factory.django.DjangoModelFactory):
    created_by=factory.SubFactory(UserFactory)

class GroupFactory(BaseFactory):
    class Meta:
        model=Group
    name=factory.Sequence(lambda n: f"group{n}")

class VisitorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Visitor
    first_name=factory.Sequence(lambda n: f'Test First Name {n}')
    last_name=factory.Sequence(lambda n: f'Test Last Name{n}')
    country='Nepal',
    address='Lamjung',
    contact_number=factory.Sequence(lambda n: f'980000000{n}')
    email=factory.Sequence(lambda n: f'someone{n}@example.com')
    emergency_contact='9811111111'
    age=18,
    group=factory.SubFactory(GroupFactory)
