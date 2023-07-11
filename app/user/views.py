from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication


from user.serializers import (
    UserSerializer,
    MyTokenObtainPairSerializer
)


class createUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class createTokenView(TokenObtainPairView):
    """Create a new auth token for user"""
    serializer_class = MyTokenObtainPairSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return the authenticated user"""
        return self.request.user
