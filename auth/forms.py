from django import forms
from django.core.exceptions import ValidationError
from django.db.models.expressions import result

from .models import CustomUser

class SignUpForm(forms.Form):

    contact = forms.CharField(max_length=150, label="Email or phone number")
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    full_name = forms.CharField(max_length=256)
    username = forms.CharField(max_length=256)

    def _clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken")
        return username

    def _clean_contact(self):
        contact = self.cleaned_data.get("contact")
        if CustomUser.email.objects.filter(email__iexact=contact).exists():
            raise ValidationError ("This email is already used")
        elif CustomUser.phone_number.objects.filter(phone_number__iexact=contact).exists():
            raise ValidationError ("This phone number is already used")
        return contact

    def _clean_password(self):
        pass

    def clean(self):
        cleaned_data = super().clean()
        contact = cleaned_data.get("contact")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        if "@" in contact:
            cleaned_data["email"] = contact
        else:
            cleaned_data["phone_number"] = contact
        return cleaned_data

