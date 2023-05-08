""" Views for user api"""

from rest_framework import generics

from user.serialiazers import UserSerializer


class createUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer
