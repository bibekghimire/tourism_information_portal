from django.test import TestCase
from activity.models import Activity,ActivityType, Destination, Route, Travel
from django.core.exceptions import ValidationError
from userprofile.factories import UserFactory
from activity.factories import ActivityTypeFactory, ActivityFactory, DestinationFactory

class TestRoute(TestCase):
    def setUp(self):
        self.user=UserFactory()
        self.destinations=DestinationFactory.create_batch(3)
        self.data={
            'created_by':self.user,
            'title': 'route1',
            'start_point':'start1',
            'end_point':'end1'
        }
    def test_create_route(self):
        route=Route.objects.create(**self.data)
        route.destinations.set(self.destinations)
        self.assertEqual(route.title, self.data['title'])
        self.assertEqual(route.start_point,self.data['start_point'])
        self.assertEqual(route.end_point,self.data['end_point'])
        for destiny in route.destinations.all():
            with self.subTest(f'test destiny:{destiny}'):
                self.assertIn(destiny,self.destinations)
class TestActivity(TestCase):
    def setUp(self):
        self.user=UserFactory()
        self.type=ActivityTypeFactory()
        self.data={
            'title':'Trekking',
            'created_by': self.user,
            'type':self.type,
        }
        
    def test_create_activity(self):
        activity=Activity.objects.create(**self.data)
        self.assertEqual(activity.title,self.data['title'])
        self.assertEqual(activity.type,self.type)
        self.assertEqual(activity.created_by,self.user)
    def test_activity_title_uniqueness(self):
        activity=Activity.objects.create(**self.data)
        with self.assertRaises(ValidationError):
            Activity.objects.create(**self.data)

class TestDestination(TestCase):
    def setUp(self):
        self.user=UserFactory()
        self.title='Destination 1'
        self.activity=ActivityFactory.create_batch(2)
        self.geo_location='test_location'
        self.data={
            'created_by':self.user,
            'title':self.title,
            'geo_location':self.geo_location
        }
    
    def test_create_destination(self):
        destiny=Destination.objects.create(**self.data)
        destiny.activity.set(self.activity)
        self.assertEqual(destiny.title, self.title)
        self.assertEqual(destiny.geo_location,self.geo_location)
    def test_destination_title_uniqueness(self):
        destiny=Destination.objects.create(**self.data)
        destiny.activity.set(self.activity)
        with self.assertRaises(ValidationError):
            Destination.objects.create(**self.data)

class TestActivityType(TestCase):
    def setUp(self):
        self.user=UserFactory()
        self.data={
            'created_by':self.user,
            'title':'adv&sports:type'
        }
    
    def test_create_activity_type(self):
        activity_type=ActivityType.objects.create(
            **self.data
        )
        self.assertEqual(activity_type.title,self.data['title'])
        self.assertEqual(activity_type.created_by,self.user)
    def test_create_activity_type_max_length(self):
        with self.assertRaises(ValidationError):
            ActivityType.objects.create(title='adv&sports:typed'*10, 
                                        created_by=self.user)

    def test_activity_type_title_uniqueness(self):
        activity_type=ActivityType.objects.create(
            **self.data
        )
        with self.assertRaises(ValidationError):
            ActivityType.objects.create(title='adv&sports:type', created_by=self.user)

