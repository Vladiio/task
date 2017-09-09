from rest_framework import viewsets
from rest_framework import views
from rest_framework import mixins
from rest_framework import authentication
from rest_framework.response import  Response


from .models import Task, CustomToken
from .serializers import  TaskSerializer
from .authentication import MasterTokenAuth, BasicTokenAuth
from .permissions import ReadUpdateDeletePerm


class TaskViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = (BasicTokenAuth,)


class AuthTokenView(views.APIView):
    authentication_classes = (MasterTokenAuth,)

    def post(self, request, *args, **kwargs):
        token = CustomToken.objects.create()
        return Response({'token': token.key})
