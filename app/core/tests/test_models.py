"""Tests for models"""

from unittest.mock import patch
from django.utils import timezone
from datetime import timedelta
from django.db import IntegrityError
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Tests for models"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_emails = [
            ['test1@example.com', 'test1@example.com'],
            ['Test2@example.com', 'Test2@example.com'],
            ['TEST3@example.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],

        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises an valueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'sample123')

    def test_create_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a new recipe is successful"""

        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=Decimal('5.00'),
            description='This is a test description'
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a new tag is successful"""

        user = create_user()
        tag = models.Tag.objects.create(
            user=user,
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_create_ingredients(self):
        """Test creating a new ingredient is successful"""

        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        expected_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, expected_path)

    def test_create_event(self):
        """Test creating a new event is successful"""

        user = create_user()
        recipe = models.Recipe.objects.create(
            user=user,
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=Decimal('5.00'),
            description='This is a test description'
        )
        start_time = timezone.now()
        end_time = start_time + timedelta(hours=1)
        event = models.Event.objects.create(
            user=user,
            recipe=recipe,
            description='Sunday lunch with family',
            start_time=start_time,
            end_time=end_time
        )

        self.assertEqual(str(event), event.title)

    def test_create_event_without_required_fields(self):
        """Test that creating an event without required fields raises an error"""
        user = create_user()
        recipe = models.Recipe.objects.create(
            user=user,
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=Decimal('5.00'),
            description='This is a test description'
        )

        with self.assertRaises(IntegrityError):
            models.Event.objects.create(
                user=user,
                recipe=recipe,
                title='',
                description='Sunday lunch with family',
                start_time=None,
                end_time=None
            )
