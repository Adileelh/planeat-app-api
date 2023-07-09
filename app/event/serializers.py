from rest_framework import serializers
from core.models import Event


class EventSerializer(serializers.ModelSerializer):
    """Serializer for the Event model"""
    class Meta:
        model = Event
        fields = ('id', 'user', 'recipe', 'title',
                  'description', 'start_time', 'end_time')
        read_only_fields = ('id', 'user')
