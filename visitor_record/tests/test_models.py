from django.test import TestCase
from django.contrib.auth.models import User
from visitor_record.models import Group
from django.core.exceptions import ValidationError
from userprofile.factories import UserFactory, UserProfileFactory

class TestGroup(TestCase):
    def setUp(self):
        self.user=UserFactory()
        self.userprofile=UserProfileFactory(user=self.user)
    def test_create_group(self):
        group=Group.objects.create(
            name='Group1',
            created_by=self.user
        )
        self.assertEqual(group.name,'Group1')
        self.assertEqual(group.created_by,self.user)
        self.assertEqual(group.author,self.userprofile.full_name)
        
    def test_group_name_unique_constraint(self):
        Group.objects.create(
            name='Group 1',
            created_by=self.user
        )
        with self.assertRaises(ValidationError):
            Group.objects.create(name="Group 1", created_by=self.user)

class TestVisitor(TestCase):
    