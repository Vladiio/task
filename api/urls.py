from django.conf.urls import url

from rest_framework.routers import  DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from .views import test, TaskViewSet, GetAuthToken


router = DefaultRouter()
router.register(r'tasks', TaskViewSet, base_name='task')


urlpatterns = [
    url(r'^$', test),
    url(r'^master-token/$', obtain_auth_token),
    url(r'^token/$', GetAuthToken.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += router.urls
