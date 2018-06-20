from django.core.mail import send_mail

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .permissions import IsOwnerOrReadOnly
from .serializers import AnonymouseUserSerializer
from .serializers import UserSerializer
from .serializers import UserIsActiveSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        user = serializer.save()
        self._send_token(user)

    @action(
        methods=['patch'],
        detail=True,
        permission_classes=[permissions.AllowAny])
    def is_active(self, request, pk):
        """This is the user activation endpoint."""

        try:
            token = Token.objects.get(key=self.request.data.get('token'))
        except Token.DoesNotExist:
            raise serializers.ValidationError({'token': 'Invalid Token'})

        if int(pk) != token.user.pk:
            raise serializers.ValidationError({'token': 'Invalid Token'})

        is_active_serializer = UserIsActiveSerializer(
            token.user, data={'is_active': True},
            context={'request': request})

        if is_active_serializer.is_valid():
            is_active_serializer.save()

        user_serializer = self.get_serializer(token.user)
        return Response(user_serializer.data)

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        Override to provide different serializer depending on the authorization
        of the user.
        """

        if self.request.user.is_authenticated():
            return UserSerializer
        return AnonymousUserSerializer

    def send_email_token(self, user):
        """
        Sends an email containing activation token to the user
        once User obj is created.
        """

        token, _ = Token.objects.get_or_create(user=user)
        message = 'token = {}'.format(token)
        send_mail(
            subject='Token for Activation'
            message=message,
            from_email=settings.EMAIL_SENDER,
            recipient_list=[user.email]
        )
