from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from userprofile.models import UserProfile
from userprofile.factories import UserFactory, UserProfileFactory

class UserListCreateTest(APITestCase):
    def setUp(self):
        # Create Admin
        self.admin=User.objects.create_user(username="admin", password="adminpass")
        self.admin_profile=UserProfileFactory(user=self.admin, role='AD')

        #create staff
        self.staff=UserFactory()
        self.staff_profile=UserProfileFactory(user=self.staff,role='ST')

        self.creator=UserFactory()
        self.creator_profile=UserProfileFactory(user=self.creator, role='CR')

        self.url = reverse('userprofile:user-list-create')

    def test_unauthenticated_user_cannot_access(self):
        response=self.client.get(self.url)
        self.assertEqual(response.status_code,401)

    def test_creator_cannot_access_user_list(self):
        self.client.force_authenticate(user=self.creator)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
    def test_staff_can_list_users(self):
        self.client.force_authenticate(user=self.staff)
        response=self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    def test_admin_can_list_users(self):
        self.client.force_authenticate(user=self.admin)
        response=self.client.get(self.url)
        self.assertEqual(response.status_code,200)
    def test_creator_cannot_create_user(self):
        self.client.force_authenticate(user=self.creator)
        data = {
            "username": "newuser1",
            "password": "newpass123"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 403)
    
    def test_staff_can_create_user(self):
        self.client.force_authenticate(user=self.staff)
        data = {
            "username": "newuser3",
            "password1": "newpass123",
            "password2": "newpass123",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
    def test_admin_can_create_user(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            "username": "newuser3",
            "password1": "newpass123",
            "password2": "newpass123",

        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
    