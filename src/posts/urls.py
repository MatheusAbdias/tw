from django.urls import include, path
from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet

app_name = "posts"

router = DefaultRouter()

router.register("", PostViewSet, basename="posts")

urlpatterns = [
    path("", include(router.urls)),
]
