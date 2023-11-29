from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls", namespace="authentication")),
    path("posts/", include("posts.urls", namespace="posts")),
]
