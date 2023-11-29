from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated

from posts.models import Post
from posts.serializers import PostSerializer


class PostViewSet(CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
