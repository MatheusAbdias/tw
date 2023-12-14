from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated

from posts.models import Post
from posts.serializers import PostSerializer


class PostViewSet(ListModelMixin, CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["owner"]
