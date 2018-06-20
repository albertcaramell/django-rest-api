from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet


router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
