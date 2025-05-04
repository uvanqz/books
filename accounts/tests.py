from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User


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


class UserLoginLogoutAPIViewTest(TestCase):
    def setUp(self):
        self.login_url = reverse('accounts:user_login')
        self.logout_url = reverse('accounts:user_logout')
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

    def test_login_nonexistent_user(self):
        response = self.client.post(self.login_url, {
            'username': 'nonexistentuser',
            'password': 'nonexistenpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def authenticate(self):
        self.client.login(username='testuser', password='testpassword123')

    def test_post_logout_authenticated(self):
        self.authenticate()
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User logged out successfully')

    def test_post_logout_unauthenticated(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
