from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from .utils import validators


UserModel = get_user_model()


class UniversalBackend(ModelBackend):
    def authenticate(self, request,login=None,password=None, **kwargs):
        user = self._get_user_by_login(login)
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def _get_user_by_login(self,login):
        try:
            if validators.validate_email_format(login):
                return UserModel.objects.get(email__iexact=login)
            elif validators.is_phone_number(login):
                return UserModel.objects.get(phone_nubmer=login)
            elif login:
                return UserModel.objects.get(username__iexact=login)

        except UserModel.DoesNotExist:
            return None

    # def _get_lookup_field(self,login):
    #     if validators.is_email(login):
    #         return "email"
    #     elif validators.is_phone_number(login):
    #         return "phone_number"
    #     elif login:
    #         return "username"
    #
    #     return None




