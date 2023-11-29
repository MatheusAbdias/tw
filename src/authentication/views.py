from rest_framework import status, viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from authentication.serializers import SignupUserSerializer


class SignupViewSet(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SignupUserSerializer
    permission_classes = [AllowAny]


class LoginViewSet(viewsets.GenericViewSet):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RefreshTokenVIew(viewsets.GenericViewSet):
    serializer_class = TokenRefreshSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
