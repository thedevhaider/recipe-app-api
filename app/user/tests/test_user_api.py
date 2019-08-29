from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_API = reverse('user:create')
TOKEN_URI = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test APIs that don't require authentication"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test if user is created using valid payload"""
        payload = {
            'email': 'haider@gmail.com',
            'password': 'testpass123',
            'name': 'Haider'
        }
        res = self.client.post(CREATE_USER_API, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_missing_fields(self):
        """Test if user is created when fields are missing"""
        payload = {
            'email': 'email',
            'password': ''
        }
        res = self.client.post(CREATE_USER_API, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_exists(self):
        """Test if the user already exists"""
        payload = {
            'email': 'haider@gmail.com',
            'password': 'testpass123'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_API, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test if password is less than 5 Characters"""
        payload = {
            'email': 'haider@gmail.com',
            'password': 'pw'
        }
        res = self.client.post(CREATE_USER_API, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test if the token is created when user payload is provided"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URI, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created with wrong creds"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass'
        }
        create_user(**payload)
        wrong_payload = {
            'email': 'test@gmail.com',
            'password': 'wrong'
        }
        res = self.client.post(TOKEN_URI, wrong_payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token not created when user does'nt exists"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass'
        }
        res = self.client.post(TOKEN_URI, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_fields(self):
        """Test that token not created when fields are missing"""
        payload = {
            'email': 'email',
            'password': ''
        }
        res = self.client.post(TOKEN_URI, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unautherized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test APIs that requires authentication"""

    def setUp(self):
        self.user = create_user(
            email='test@gmail.com',
            password='testpass123',
            name='testname'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retreiving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name
        })

    def test_post_me_not_allowed(self):
        """Test that post is not allowed on me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_profile_success(self):
        """Test updating the user profile for authenticated user"""
        payload = {
            'email': 'newtest@gmail.com',
            'password': 'newpassword'
        }
        res = self.client.patch(ME_URL, payload)

        # Refresh the user object with latest values from db
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, payload['email'])
        self.assertTrue(self.user.check_password(payload['password']))
