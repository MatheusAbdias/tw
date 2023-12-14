from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from authentication.models import User
from authentication.serializers import SignupUserSerializer, UserSerializer


class UsersViewSet(ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    @action(detail=True, methods=["POST"])
    def follow(self, request, pk=None):
        user = self.get_object()
        request.user.follow(user)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["POST"])
    def unfollow(self, request, pk=None):
        user = self.get_object()
        request.user.unfollow(user)

        return Response(status=status.HTTP_204_NO_CONTENT)


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
