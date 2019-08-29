from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_API = reverse('user:create')
TOKEN_URI = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):

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
