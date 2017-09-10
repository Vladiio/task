from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken


from .models import Task, CustomToken
from .serializers import TaskSerializer
from .authentication import CustomTokenAuth


class TaskViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = (CustomTokenAuth,)
    permission_classes = ()


class AuthTokenView(ObtainAuthToken):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        token = CustomToken.objects.create()
        return Response({'token': token.key})
