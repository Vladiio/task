from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import status

from .utils import gen_random_string, get_token
from .models import Task


User = get_user_model()


class AuthTokenViewTests(TestCase):

    def setUp(self):
        self.credentials = {'username': 'test',
                            'password': '123'}

        self.client = APIClient()
        self.user = User.objects.create_user(**self.credentials)
        response = self.client.post(reverse('master-token'),
                                    self.credentials,
                                    format='json')
        self.client.credentials(HTTP_AUTHORIZATION=get_token(response))

    def test_without_authorization_header(self):
        self.client.credentials()
        response = self.client.post(reverse('auth-token'))
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_with_invalid_authorization_header(self):
        token = 'Token ' + gen_random_string()
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.post(reverse('auth-token'))
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_valid_authorization_header(self):
        response = self.client.post(reverse('auth-token'))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_get_method_is_forbidden(self):
        response = self.client.get(reverse('auth-token'))
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)


class MasterTokenViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_without_credentials(self):
        response = self.client.post(reverse('master-token'))
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)


class TaskViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.credentials = {'username': 'test',
                            'password': '123'}
        User.objects.create_user(**self.credentials)

        response = self.client.post(reverse('master-token'),
                                    self.credentials,
                                    format='json')
        master_token = get_token(response)
        # retrieve custom token with master-token
        self.client.credentials(HTTP_AUTHORIZATION=master_token)
        response = self.client.post(reverse('auth-token'))
        self.custom_token = get_token(response)

        self.client.credentials()

    def test_get_without_token(self):
        response = self.client.get(reverse('tasks-list'))
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_post_with_valid_token(self):
        task_data = {
            'title': 'new',
            'action': 'move',
            'start': timezone.now()
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.custom_token)

        response = self.client.post(reverse('tasks-list'), task_data)
        self.assertEqual(response.status_code,

                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_with_valid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.custom_token)
        response = self.client.get(reverse('tasks-list'))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_get_with_invalid_token(self):
        token = 'Token ' + gen_random_string()
        self.client.credentials(HTTP_AUTHORIZATION=token)
        response = self.client.get(reverse('tasks-list'))
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_patch_with_valid_token(self):
        task = self.create_task_object()
        action = task.action.lower()

        self.client.credentials(HTTP_AUTHORIZATION=self.custom_token)
        response = self.client.patch(reverse('tasks-detail',
                                     kwargs={'pk': task.pk}),
                                     {'action': action})

        self.assertEqual(response.data.get('action'), action)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_with_valid_token(self):
        task = self.create_task_object()
        self.client.credentials(HTTP_AUTHORIZATION=self.custom_token)

        response = self.client.delete(reverse('tasks-detail',
                                      kwargs={'pk': task.pk}))
        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT)

    @staticmethod
    def create_task_object():
        task_data = {
            'title': 'Wake up',
            'action': 'Wake up and go to work',
            'start': timezone.now() + timezone.timedelta(days=1)
        }
        task = Task.objects.create(**task_data)
        task.save()
        return task
