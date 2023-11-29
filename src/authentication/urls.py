from django.urls import include, path
from rest_framework import routers

from authentication.views import LoginViewSet, RefreshTokenVIew, SignupViewSet

app_name = "authentication"

router = routers.DefaultRouter()
router.register("signup", SignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")
router.register("refresh", RefreshTokenVIew, basename="refresh-token")

urlpatterns = [
    path("", include(router.urls)),
]
