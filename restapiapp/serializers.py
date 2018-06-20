from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for handling authorized users."""

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'password', 'first_name', 'last_name', 'is_active',
            'url', 'current_password'
        )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('is_active',)

    current_password = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        """Override create method so password can be saved properly."""

        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        """Override update method to handle password change."""

        current_password = validated_data.get('current_password')
        for attr, value in validated_data.items():
            if attr == 'password':
                if not instance.check_password(current_password):
                    raise serializers.ValidationError(
                        {'current_password': 'invalid password'})
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class AnonymousUserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for handling anonymous users."""

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'password', 'first_name', 'last_name',
            'is_active', 'token', 'url'
        )

        read_only_fields = ('is_active',)
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'write_only': True},
            'last_name': {'write_only': True}
        }

    def create(self, validated_data):
        """Override create method so password can be saved properly."""

        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserIsActiveSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for updating the `is_active` field of the user."""

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'is_active', 'url',)
        read_only_fields = ('first_name', )
