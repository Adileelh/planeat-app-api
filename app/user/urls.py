"""Urls mapping for user api."""

from django.urls import path
from user import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'user'

urlpatterns = [
    path('create/',
         views.createUserView.as_view(),
         name='create'),
    path('token/',
         views.createTokenView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('me/',
         views.ManageUserView.as_view(),
         name='me'),
]
