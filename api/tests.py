import random
import string

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


from .views import AuthTokenView


test_username = 'test'
test_password = '123'

User = get_user_model()


class AuthTokenViewTests(TestCase):
    def setUp(self):
        credentials = {'username': test_username,
                       'password': test_password}

        self.client = APIClient()
        self.user = User.objects.create_user(username=test_username,
                                             password=test_password)
        response = self.client.post(reverse('master-token'),
                                    credentials, format='json')
        token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_without_authorization_header(self):
        self.client.credentials()
        response = self.client.post(reverse('auth-token'))
        self.assertEqual(response.status_code, 403)

    def test_with_invalid_authorization_header(self):
        token = 'Token ' + gen_random_string()
        self.client.credentials(HTTP_AUTHORIZATION=token)
        request = self.client.post(reverse('auth-token'))
        self.assertEqual(request.status_code, 403)


def gen_random_string(max_length=20,
                      chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(max_length))
