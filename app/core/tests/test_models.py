from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email="test@gmail.com", password="testpass"):
    """"Create sample user"""
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """Test the string representation of tag"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Vegan"
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)
