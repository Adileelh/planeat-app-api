from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Event, Recipe

from event.serializers import EventSerializer

EVENTS_URL = reverse('event:event-list')


def detail_url(event_id):
    """Return event detail URL"""
    return reverse('event:event-detail', args=[event_id])


def create_event(user, **params):
    """Create a sample event"""
    defaults = {
        'start_time': timezone.now(),
        'end_time': timezone.now() + timedelta(hours=1),
        'recipe': create_recipe(user=user),
    }
    defaults.update(params)

    event = Event.objects.create(user=user, **defaults)

    return event


def create_recipe(user, **params):
    """Create a sample recipe"""
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'https://www.google.com',
    }

    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)

    return recipe


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicEventApiTests(TestCase):
    """Test the publicly available event API"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required for retrieving events"""
        res = self.client.get(EVENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEventApiTests(TestCase):
    """Test the authorized user event API"""

    def setUp(self):
        self.user = create_user(
            email='test@event.com',
            password='testpass',
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_events(self):
        """Test retrieving events"""
        recipe1 = create_recipe(user=self.user)
        recipe2 = create_recipe(user=self.user)

        start_time = timezone.now()
        end_time = start_time + timedelta(hours=1)

        Event.objects.create(
            user=self.user,
            start_time=start_time,
            end_time=end_time,
            recipe=recipe1
        )
        Event.objects.create(
            user=self.user,
            start_time=start_time,
            end_time=end_time,
            recipe=recipe2)

        res = self.client.get(EVENTS_URL)

        events = Event.objects.all().order_by('-recipe__title')
        serializer = EventSerializer(events, many=True)

        # Check that the returned data matches the expected data
        expected_data = serializer.data
        actual_data = res.data

        # Compare the data without taking order into account
        self.assertCountEqual(actual_data, expected_data)

    def test_event_list_limited_to_user(self):
        """Test list of events is limited to authenticated user"""
        other = create_user(
            email='other@example.com',
            password='testpass123',
        )
        create_recipe(user=other)
        create_event(user=other)

        create_recipe(user=self.user)
        create_event(user=self.user)

        res = self.client.get(EVENTS_URL)

        events = Event.objects.filter(user=self.user)
        serializer = EventSerializer(events, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_event_detail_view(self):
        """Test viewing an event detail"""
        event = create_event(user=self.user)

        url = detail_url(event.id)
        res = self.client.get(url)

        serializer = EventSerializer(event)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_event(self):
        """Test creating a new event"""
        recipe = create_recipe(user=self.user)

        payload = {
            'title': recipe.title,
            'start_time': timezone.now() + timedelta(days=1),
            'end_time': timezone.now() + timedelta(days=1, hours=1),
            'recipe': recipe.id,
        }

        res = self.client.post(EVENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        event = Event.objects.get(id=res.data['id'])

        # Check the title against the recipe's title
        self.assertEqual(event.title, recipe.title)
        self.assertEqual(event.start_time, payload['start_time'])
        self.assertEqual(event.end_time, payload['end_time'])
        self.assertEqual(event.recipe.id, payload['recipe'])

    def test_update_event(self):
        """Test updating an event"""
        event = create_event(user=self.user)
        recipe = create_recipe(user=self.user)

        payload = {
            'start_time': timezone.now() + timedelta(days=2),
            'end_time': timezone.now() + timedelta(days=2, hours=1),
            'recipe': recipe.id,
        }

        url = detail_url(event.id)
        res = self.client.patch(url, payload)

        event.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(event.title, event.recipe.title)
        self.assertEqual(event.start_time, payload['start_time'])
        self.assertEqual(event.end_time, payload['end_time'])
        self.assertEqual(event.recipe.id, payload['recipe'])

    def test_update_event_by_other_user(self):
        """Test that another user cannot update an event"""
        other_user = create_user(
            email='other@event.com',
            password='testpass',
        )
        event = create_event(user=self.user)

        self.client.force_authenticate(other_user)
        url = detail_url(event.id)
        payload = {
            'start_time': timezone.now() + timedelta(days=2),
            'end_time': timezone.now() + timedelta(days=2, hours=1),
            'recipe': create_recipe(user=other_user).id,
        }
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_event(self):
        """Test deleting an event"""
        event = create_event(user=self.user)

        url = detail_url(event.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=event.id).exists())

    def test_delete_event_by_other_user(self):
        """Test that another user cannot delete an event"""
        other_user = create_user(
            email='other@event.com',
            password='testpass',
        )
        event = create_event(user=self.user)

        self.client.force_authenticate(other_user)
        url = detail_url(event.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
