""" manage events in the database"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Event
from event import serializers


class EventViewSet(viewsets.ModelViewSet):
    """Manage events in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new event"""
        serializer.save(user=self.request.user)
