from rest_framework import authentication
from rest_framework.authtoken.models import Token
from rest_framework import exceptions


from .models import CustomToken
from .utils import fetch_token


class MasterTokenAuth(authentication.BaseAuthentication):

    def authenticate(self, request):
        fetch_token(request, Token)


class BasicTokenAuth(authentication.BaseAuthentication):

    def authenticate(self, request):
        fetch_token(request, CustomToken)

