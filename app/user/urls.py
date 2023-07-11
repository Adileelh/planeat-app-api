"""Urls mapping for user api."""

from django.urls import path, include

app_name = "user"

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
