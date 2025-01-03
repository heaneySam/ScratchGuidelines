# tableapp/authentication.py

from rest_framework import authentication, exceptions
from django.conf import settings

class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    Simple API Key Authentication.
    Clients should authenticate by passing the API Key in the 'X-API-KEY' header.
    """

    def authenticate(self, request):
        api_key = request.headers.get('X-API-KEY')

        if not api_key:
            return None  # No API key provided

        if api_key != settings.SIMPLE_API_KEY:
            raise exceptions.AuthenticationFailed('Invalid API Key')

        # Optionally, associate the API key with a user or return a dummy user
        # For simplicity, we'll return an anonymous user
        return (None, None)
