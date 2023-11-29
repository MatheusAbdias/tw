from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ["id", "content", "owner", "created_at"]
        read_only_fields = ["created_at"]
