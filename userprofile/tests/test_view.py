from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from userprofile.factories import UserFactory, UserProfileFactory

class TestUserListCreateView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # cls.client=APIClient()
        cls.admin=UserFactory()
        cls.admin_profile=UserProfileFactory(user=cls.admin, role='AD')

        cls.staff=UserFactory()
        cls.staff_profile=UserProfileFactory(user=cls.staff, role='ST')

        cls.creator=UserFactory()
        cls.creator_profile=UserProfileFactory(user=cls.creator, role='CR')

        cls.create_url = reverse('userprofile:user-list-create')

    def test_admin_can_create_user(self):
        self.client.force_authenticate(user=self.admin)
        response=self.client.post(self.create_url,{
            'username':'newusername',
            'password1':'testpass',
            'password2':'testpass'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_staff_can_create_user(self):
        self.client.force_authenticate(user=self.staff)
        response=self.client.post(self.create_url,{
            'username':'username2',
            'password1':'testpass',
            'password2':'testpass'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_creator_cannot_create_user(self):
        self.client.force_authenticate(user=self.creator)
        response=self.client.post(self.create_url,{
            'username':'username32',
            'password1':'testpass',
            'password2':'testpass'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
