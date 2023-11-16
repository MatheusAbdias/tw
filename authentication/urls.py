from django.urls import include, path
from rest_framework import routers

from authentication.views import SignupViewSet

app_name = "authentication"

router = routers.DefaultRouter()
router.register("signup", SignupViewSet, basename="signup")

urlpatterns = [path("", include(router.urls))]
