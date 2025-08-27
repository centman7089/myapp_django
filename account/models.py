from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken

AUTH_PROVIDERS = {
    'email': 'email',
    'google': 'google',
    'github': 'github',
    'facebook': 'facebook'
}

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))

    # ✅ New fields from registration form
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Phone Number"))
    address = models.TextField(blank=True, null=True, verbose_name=_("Address"))
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("City"))
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Country"))

    # Default auth fields
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    auth_provider = models.CharField(max_length=50, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def tokens(self):
        """Generate JWT tokens"""
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f'{self.user.first_name} passcode'
