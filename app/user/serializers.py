"""
Serializers for the user API view.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers #import serializers base class from rest_framework - convert objects from and into object (JSON -> python object, python object -> JSON)


class UserSerializer(serializers.ModelSerializer): #ModelSerializer - automatic validate and save things in models as defined in serializers
    """Serializer for the user object."""

    class Meta: # tell django rest framework the model and fields, additional args are passed to the serializers
        model = get_user_model()
        fields = ['email', 'password', 'name'] # fields available through the serializer, fields in the request that is saved in the model that is created.
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}} # extra keyword arguments, extra metadata to different fields, min_length - validation, returns 400 if not met

    def create(self, validated_data): #validated data already from the serializer
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style = {'input_type': 'password'}, # hide characters
        trim_whitespace=False, # whitespace on the end of the password deliberate
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization') # raise 400 

        attrs['user'] = user
        return attrs



