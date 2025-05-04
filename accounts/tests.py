from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User

from .serializers import UserSerializer


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "email": "test@example.com",
        }

    def test_valid_user_serializer(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_user_serializer(self):
        invalid_user_data = self.user_data.copy()
        invalid_user_data["email"] = "invalidemail"
        serializer = UserSerializer(data=invalid_user_data)
        self.assertFalse(serializer.is_valid())


class UserRegistrationAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("accounts:user_registration")
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "email": "test@example.com",
        }

    def test_user_registration_successful(self):
        response = self.client.post(
            self.register_url, self.user_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], self.user_data["username"])

    def test_user_registration_invalid_email(self):
        invalid_data = self.user_data.copy()
        invalid_data["email"] = "invalidemail"
        response = self.client.post(
            self.register_url, invalid_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_missing_field(self):
        invalid_data = self.user_data.copy()
        del invalid_data["username"]
        response = self.client.post(
            self.register_url, invalid_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginAPIViewTest(TestCase):
    def setUp(self):
        self.login_url = reverse('accounts:user_login')
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

    def test_login_successful(self):
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'User logged in successfully')

    def test_login_wrong_password(self):
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_login_nonexistent_user(self):
        response = self.client.post(self.login_url, {
            'username': 'nonexistentuser',
            'password': 'nonexistenpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_empty_fields(self):
        response = self.client.post(self.login_url, {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)


class UserLogoutAPIViewTest(TestCase):
    def setUp(self):
        self.logout_url = reverse('accounts:user_logout')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )

    def authenticate(self):
        self.client.login(username='testuser', password='testpassword123')

    def test_post_logout_authenticated(self):
        self.authenticate()
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User logged out successfully')

    def test_get_logout_authenticated(self):
        self.authenticate()
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User logged out successfully')

    def test_post_logout_unauthenticated(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_logout_unauthenticated(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
