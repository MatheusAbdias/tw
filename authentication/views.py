from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny

from authentication.serializers import SignupUserSerializer


class SignupViewSet(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SignupUserSerializer
    permission_classes = [AllowAny]
