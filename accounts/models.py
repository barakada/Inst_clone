from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from src.settings import TIME_ZONE
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_("email address"),unique=True,blank=True,null=True)
    username = models.CharField(max_length=200,unique=True)
    phone_number = models.CharField(max_length=20,unique=True,blank=True,null=True)
    full_name = models.CharField(max_length=200)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username



