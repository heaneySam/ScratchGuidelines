# tableapp/authentication.py

from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth.models import User

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

        try:
            # Fetch the user associated with the API key
            user = User.objects.get(username='apiuser')  # Replace 'apiuser' with your designated username
        except User.DoesNotExist:
            # Optionally, create the user if it doesn't exist
            user = User.objects.create_user(username='apiuser', password=None)
            user.is_staff = False
            user.is_superuser = False
            user.save()

        return (user, None)
