from rest_framework.test import APITestCase, APIRequestFactory
from activity.serializers import *
from activity import models
from userprofile.factories import UserFactory
from activity import factories 
import time
start=time.time()

class BaseTestClass(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Runs once per class
        cls.user = UserFactory()
        cls.update_user = UserFactory()
        cls.types_pool=factories.ActivityTypeFactory.create_batch(5,created_by=cls.user)
        cls.activity_pool = factories.ActivityFactory.create_batch(5, created_by=cls.user,type=cls.types_pool[0])
        cls.destinations_pool = factories.DestinationFactory.create_batch(5, created_by=cls.user,activity=cls.activity_pool)
        cls.routes_pool = factories.RouteFactory.create_batch(5, created_by=cls.user,destinations=cls.destinations_pool)
        cls.travel_pool = factories.TravelFactory.create_batch(
            5,
            activities=cls.activity_pool,
            routes=cls.routes_pool,
            destinations=cls.destinations_pool,
            created_by=cls.user
        )
    def setUp(self):
        # Runs before each test method
        self.factory = APIRequestFactory()
    def get_request(self,method='post', url='fake/url', user=None):
        if method.lower()=='post':
            request= self.factory.post(url)
            request.user=user or self.user
        elif method.lower()=='get':
            request= self.factory.get(url)
        elif method.lower()=='put':
            request= self.factory.put(url)
            request.user=user or self.update_user
        elif method.lower()=='patch':
            request= self.factory.patch(url)
            request.user=user or self.update_user
        elif method.lower()=='delete':
            request= self.factory.delete(url)
            request.user=user or self.update_user
        else:
            raise ValueError(f"Unsupported method {method}")
        return request
    

class TestTravelSerializer(BaseTestClass):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # cls.types=cls.types_pool
        cls.activities=cls.activity_pool
        cls.routes=cls.routes_pool
        cls.destinations=cls.destinations_pool
        cls.travels=cls.travel_pool
        cls.data={
            'title':"Travell Test",
            'descriptions':'Desctiption for Travel Test',
            'duration':5,
            'difficulty':'easy',
            'max_altitude':2500,
            'min_altitude':200,
            'distance':3,
            'best_season':'summer',
            'required_permits':'',
            'is_guided_only':False,
            'activities':[activity.title for activity in cls.activities],
            'routes':[route.title for route in cls.routes],
            'destinations':[destination.title for destination in cls.destinations],
        }
    def setUp(self):
        super().setUp()
        # self.activities = self.__class__.activities
        # self.routes = self.__class__.routes
        # self.destinations = self.__class__.destinations
        self.data = self.__class__.data
        self.travels=self.__class__.travels
        self.request = self.get_request()

    def test_create_serializer(self):
        data=self.data
        serializer=TravelCreateSerializer(data=data,context={'request':self.request})
        self.assertTrue(serializer.is_valid(),serializer.errors)
        for field,value in data.items():
            with self.subTest(f'Testing {field}'):
                self.assertEqual(value,serializer.data[field])

    def test_list_detail_serialization(self):
        travels=self.travels
        travels = Travel.objects.prefetch_related(
                'activities', 'routes', 'destinations'
            ).filter(pk__in=[t.pk for t in travels])
        serializer=TravelListSerializer(travels,many=True)
        serialzier_d=TravelCreateSerializer(travels,many=True)
        with self.subTest("testing List"):
            self.assertEqual(len(serializer.data),len(travels))
            for travel,serialzied in zip(travels,serializer.data):
                self.assertEqual(travel.title,serialzied['title'])
        with self.subTest("Testing details"):
            self.assertEqual(len(travels),len(serialzier_d.data))
            for travel,serialized in zip(travels,serialzier_d.data):
                for field in self.data.keys():
                    if field in ['activities','routes','destinations']:
                        self.assertEqual(serialized[field],[obj.title for obj in getattr(travel,field).all()])
                        continue
                    with self.subTest(f'testing {field}'):
                        self.assertEqual(serialized[field],getattr(travel,field))
            print("duration: ", abs(start-time.time()))

        
class TestRouteSerialization(BaseTestClass):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.destinations=cls.destinations_pool
        cls.routes=cls.routes_pool
        cls.data={
            'title':'Test Route',
            'start_point':'start route 1',
            'end_point':'end route 2',
            'destinations':[destination.title for destination in cls.destinations]
        }

    def setUp(self):   
        super().setUp()
        self.request=self.get_request() 
        self.routes = self.__class__.routes
        # self.destinations = self.__class__.destinations
        self.data = self.__class__.data
        
        
    def test_create_serialzier(self):
        data=self.data
        serializer=RouteCreateSerializer(data=data, context={'request':self.request})
        self.assertTrue(serializer.is_valid(),serializer.errors)
        route=serializer.save()
        self.assertEqual(route.title, data['title'])
        self.assertEqual(route.start_point,data['start_point'])
        self.assertEqual(route.end_point,data['end_point'])
        self.assertEqual(route.created_by,self.user)
        self.assertEqual(set(route.destinations.all()),set(self.destinations))
    
    def test_list_detail_serialization(self):
        routes=self.routes
        routes=Route.objects.prefetch_related(
            'destinations'
        ).filter(pk__in=[t.pk for t in routes])
        with self.subTest("Testing List"):
            serializer=RouteListSerializer(routes, many=True)
            self.assertEqual(len(routes),len(serializer.data))
            for route,serialized in zip(routes,serializer.data):
                self.assertEqual(route.title,serialized['title'])
        with self.subTest("Testing for detaila"):
            serializer=RouteCreateSerializer(routes,many=True)
            for route,serialized in zip(routes,serializer.data):
                self.assertEqual(route.title,serialized['title'])
                self.assertEqual(route.start_point,serialized['start_point'])
                self.assertEqual(route.end_point,serialized['end_point'])
                destinations=[route.title for route in route.destinations.all()]
                self.assertEqual(set(destinations),set(serialized['destinations']))


class TestDestinationSerializer(BaseTestClass):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.activities=cls.activity_pool
        cls.destinations=cls.destinations_pool
        cls.data={
            'title':'Destiny 1',
            'geo_location':'geo_point 1',
            'activity':[activity.title for activity in cls.activities]
        }
    def setUp(self):
        super().setUp()
        self.request=self.get_request()
        self.data = self.__class__.data
        self.destinations=self.__class__.destinations
    
    def test_destination_create(self):
        data=self.data
        serializer=DestinationCreateSerializer(
            data=data,
            context={'request':self.request}
        )
        self.assertTrue(serializer.is_valid(),serializer.errors)
        destination=serializer.save()
        self.assertEqual(destination.title,data['title'])
        self.assertEqual(destination.created_by,self.user)
        self.assertEqual(destination.geo_location,data['geo_location'])
    
    def test_destination_list_details(self):
        destinations=self.destinations
        destinations=Destination.objects.prefetch_related(
            'activity'
        ).filter(pk__in=[t.pk for t in destinations])
        serializer=DestinationListSerializer(destinations, many=True)
        with self.subTest("testing List Serialization"):
            self.assertEqual(len(serializer.data),5)
            for obj,serialized in zip(destinations,serializer.data):
                with self.subTest(f"Testing:{obj.title} "):
                    self.assertEqual(obj.title,serialized['title'])
                    self.assertEqual(obj.id,serialized['id'])
        with self.subTest("testing Detail Serialization"):
            destinations=Destination.objects.all()
            
            serializer_d=DestinationCreateSerializer(destinations,many=True)
            
            self.assertEqual(len(serializer_d.data),5)
            for obj,serialized in zip(destinations,serializer_d.data):
                with self.subTest(f"Testing:{obj.title} "):
                    self.assertEqual(obj.title,serialized['title'])
                    #self.assertEqual(obj.id,serialized['id'])
                    activities=[activity.title for activity in obj.activity.all()]
                    self.assertEqual(set(activities),set(serialized['activity']))
                    self.assertEqual(obj.geo_location,serialized['geo_location'])


class TestActivitySerializer(BaseTestClass):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.types=cls.types_pool
        cls.activities=cls.activity_pool
    def setUp(self):
        super().setUp()
        self.request=self.get_request()
        self.activity_type=self.__class__.types[0]
        self.activities=self.__class__.activities
        self.data={
            'title':'old activity',
            'type':self.activity_type.title
        }
        
    def test_activity_create_serializer(self):
        request=self.get_request()
        data=self.data
        serializer=ActivityCreateSerialzier(
            data=data,
            context={'request':request}
        )
        self.assertTrue(serializer.is_valid(),serializer.errors)
        activity=serializer.save()
        self.assertEqual(activity.title,data['title'])
        self.assertEqual(activity.created_by,self.user)
    
    def test_activity_serializer(self):
        activities=self.activity_pool
        activities=Activity.objects.prefetch_related(
            'type'
        ).filter(pk__in=[t.pk for t in activities])

        list_serializer=ActivityListSerializer(activities, many=True)
        detail_serializer=ActivityCreateSerialzier(activities,many=True)
        self.assertEqual(len(list_serializer.data), 5)
        self.assertEqual(len(detail_serializer.data),5)
        for obj,serialized,detail in zip(activities,list_serializer.data,detail_serializer.data):
            with self.subTest(f"testing: {obj.title}"):
                self.assertEqual(serialized['title'],obj.title)
                self.assertEqual(ActivityType.objects.get(title=detail['type']),obj.type)
                self.assertEqual(detail['title'],obj.title)

class TestActivityTypeSerializer(BaseTestClass):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.types=cls.types_pool
    def setUp(self):
        super().setUp()
        self.request=self.get_request()
        self.types=self.__class__.types
        self.data={"title": "Adventure and Sports"}

    def test_activity_type_create(self):
        request = self.get_request(user=self.user)
        # request.user=self.user
        data = self.data
        serializer=ActivityTypeSerializer(
            data=data,
            context={'request':request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance=serializer.save()
        self.assertEqual(instance.title,data['title'])
        self.assertEqual(instance.created_by,self.user)
    
    def test_activity_type_update(self):
        request=self.get_request('put')
        activity_type=self.types[0]
        serializer=ActivityTypeSerializer(
            instance=activity_type,
            data={'title':'new updated title'},
            context={'request':request}
        )
        self.assertTrue(serializer.is_valid(),serializer.errors)
        updated_instance=serializer.save()
        self.assertEqual(updated_instance.title,'new updated title')
        self.assertEqual(updated_instance.last_modified_by,self.update_user)

