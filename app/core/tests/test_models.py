from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_user_created_with_email_is_successful(self):
        """This function checks if user is created with given email"""
        email = "mohdhaider30@gmail.com"
        password = "Testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "mohdhaider30@GMAIL.com"
        user = get_user_model().objects.create_user(email, "Test123")
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, password="Test")

    def test_create_superuser(self):
        """Test creating new superuser"""
        user = get_user_model().objects.create_superuser(
            'mohdhaider30@gmail.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
