from rest_framework import authentication
from rest_framework.authtoken.models import Token
from rest_framework import exceptions


class MasterTokenAuth(authentication.BaseAuthentication):

    def authenticate(self, request):
        token_header = request.META.get('HTTP_AUTHORIZATION')

        if not token_header:
            raise exceptions.AuthenticationFailed('Token was not provided')

        try:
            key = token_header.split(' ')[1]
            token = Token.objects.get(key=key)
        except IndexError:
            raise exceptions.AuthenticationFailed('Invalid token header')
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')
