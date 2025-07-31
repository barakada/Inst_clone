import re
import phonenumbers
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from ..models import CustomUser


def is_phone_number(value: str) -> bool:
    try:
        number = phonenumbers.parse(value, None)
        return phonenumbers.is_valid_number(number)
    except phonenumbers.NumberParseException:
        return False


def validate_email_format(email: str):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def validate_email_uniqueness(email: str):
    if CustomUser.objects.filter(email__iexact=email).exists():
        raise ValidationError("This email is already used.")


def validate_phone_uniqueness(phone: str):
    if CustomUser.objects.filter(phone_number__iexact=phone).exists():
        raise ValidationError("This phone number is already used.")


def validate_username_uniqueness(username: str):
    if CustomUser.objects.filter(username__iexact=username).exists():
        raise ValidationError("This username is already taken.")


def validate_passwords_match(password1: str, password2: str):
    if password1 and password2 and password1 != password2:
        raise ValidationError("Passwords do not match.")
