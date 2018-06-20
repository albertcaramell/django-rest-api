from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'^api/v1/', include('restapiapp.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
]
