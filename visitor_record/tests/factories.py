import factory
from faker import Faker
from django.contrib.auth import get_user_model
from visitor_record.models import Group, Visitor
from userprofile.factories import UserFactory

User=get_user_model()

class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Group
    name=factory.Sequence(lambda n: f"group{n}")
    created_by=factory.SubFactory(UserFactory)


