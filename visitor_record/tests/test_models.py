from django.test import TestCase
from django.contrib.auth.models import User
from visitor_record.models import Group, Visitor
from django.core.exceptions import ValidationError
from userprofile.factories import UserFactory, UserProfileFactory
from ..factories import GroupFactory
from activity.factories import RouteFactory


class TestGroup(TestCase):
    def setUp(self):
        self.user=UserFactory()
        self.userprofile=UserProfileFactory(user=self.user)
    def test_create_group(self):
        group=Group.objects.create(
            name='Group1',
            created_by=self.user
        )
        group.save()
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
    def setUp(self):
        self.user=UserFactory()
        self.group=GroupFactory()
        self.route=RouteFactory.create_batch(2)
        self.data={
            'first_name':'Test First Name',
            'last_name':'Test Last Name',
            'country':'Nepal',
            'address':'Lamjung',
            'contact_number':'9800000000',
            'email':'someone@example.com',
            'emergency_contact':'9811111111',
            'age':18,
            'group':self.group,
            'created_by':self.user
        }
    def test_visitor_create_valid_data(self):
        visitor=Visitor.objects.create(**self.data)
        visitor.route.set(self.route)
        visitor.save()
        for field,value in self.data.items():
            with self.subTest(f'Testing: {field}'):
                self.assertEqual(getattr(visitor,field),self.data[field])
        with self.subTest("testing routes"):
            self.assertEqual(set(visitor.route.all()), set(self.route))
    
            
    
