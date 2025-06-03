import re

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from booking.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=128, write_only=True)

    # password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'password',
            're_password',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        username = attrs.get('username')
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        role = attrs.get('role')
        password = attrs.get('password')
        re_password = attrs.get('re_password')

        if not re.match(r'^[a-zA-Z0-9_]*$', username):
            raise serializers.ValidationError(
                {"username": "Username must contain Latin characters, numbers and underscores"})

        if not re.match(r'^[a-zA-Z]*$', first_name):
            raise serializers.ValidationError({"first_name": "First name must contain Latin characters"})

        if not re.match(r'^[a-zA-Z]*$', last_name):
            raise serializers.ValidationError({"last_name": "Last name must contain Latin characters"})

        if role == "ADMIN":
            raise serializers.ValidationError({"role": "You can choose just LESSOR or RENTER"})

        try:
            validate_password(password)
        except ValidationError as err:
            raise serializers.ValidationError(err.messages)

        if password != re_password:
            raise serializers.ValidationError({"password": "Passwords don't match"})

        return attrs

    def create(self, validated_data):
        validated_data.pop('re_password')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user