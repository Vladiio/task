from rest_framework import authentication
from rest_framework import exceptions


from .models import CustomToken


class CustomTokenAuth(authentication.BaseAuthentication):

    def authenticate(self, request):
        token_header = request.META.get('HTTP_AUTHORIZATION')

        if not token_header:
            raise exceptions.AuthenticationFailed('Token was not provided')

        try:
            key = token_header.split(' ')[1]
            token = CustomToken.objects.get(key=key)
        except IndexError:
            raise exceptions.AuthenticationFailed('Invalid token header')
        except CustomToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')
