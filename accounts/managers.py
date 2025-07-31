from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username,full_name, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not username:
            raise ValueError(_("The username must be set"))

        is_super = extra_fields.get("is_superuser",False)

        if not is_super:

            email = extra_fields.get("email")
            phone = extra_fields.get("phone_number")
            if not email and not phone:
                raise ValueError(_("The email or phone_number must be set"))
        if extra_fields.get("email"):
            extra_fields["email"] = self.normalize_email(extra_fields["email"])

        user = self.model(username=username,full_name=full_name or "", **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(username=username, full_name="", password=password, **extra_fields)
