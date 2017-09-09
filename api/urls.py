from django.conf.urls import url

from rest_framework.routers import  DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import TaskViewSet, AuthTokenView

router = DefaultRouter()
router.register(r'', TaskViewSet, base_name='tasks')

urlpatterns = [
    url(r'^master-token/$', obtain_auth_token, name='master-token'),
    url(r'^auth-token/$', AuthTokenView.as_view(), name='auth-token'),
]

urlpatterns += router.urls
