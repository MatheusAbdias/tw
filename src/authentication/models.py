from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(unique=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts.",
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    following = models.ManyToManyField("self", related_name="followers", blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class EmailAlreadyExistsError(ValidationError):
        default_detail = _("A user with that email already exists.")
        default_code = "email_already_exists"

    class UsernameAlreadyExistsError(ValidationError):
        default_detail = _("A user with that username already exists.")
        default_code = "username_already_exists"

    class UserAlreadyFollowedError(ValidationError):
        default_detail = _("You already follow this user")
        default_code = "user_already_followed"

    class UserNotFollowedError(ValidationError):
        default_detail = _("You don't follow this user")
        default_code = "user_not_followed"

    class UserFollowYourSelfError(ValidationError):
        default_detail = _("You cannot follow yourself")
        default_code = "user_follow_yourself"

    class Meta:
        ordering = ["email"]
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return self.email

    @classmethod
    def validate_email(cls, email: str):
        email = cls.objects.normalize_email(email).lower()
        if cls.objects.filter(email=email).exists():
            raise cls.EmailAlreadyExistsError

        return email

    @classmethod
    def validate_username(cls, username: str):
        username = username.lower()
        if cls.objects.filter(username=username).exists():
            raise cls.UsernameAlreadyExistsError

        return username

    def follow(self, user):
        if self.id == user.id:
            raise self.UserFollowYourSelfError

        if self.following.filter(pk=user.pk).exists():
            raise self.UserAlreadyFollowedError
        self.following.add(user)

    def unfollow(self, user):
        if not self.following.filter(pk=user.pk).exists():
            raise self.UserNotFollowedError

        self.following.remove(user)
