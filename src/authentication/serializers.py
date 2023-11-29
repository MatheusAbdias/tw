from rest_framework import serializers

from authentication.models import User


class SignupUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_email(self, email: str):
        return User.validate_email(email)

    def validate_username(self, username: str):
        return User.validate_username(username)
