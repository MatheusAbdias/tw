from django.db import models


class Post(models.Model):
    owner = models.ForeignKey("authentication.User", on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"Post: {self.content} by {self.owner.username}"
