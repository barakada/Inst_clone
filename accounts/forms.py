from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .utils import validators
from .models import CustomUser

class SignUpForm(forms.Form):
    contact = forms.CharField(max_length=150, label="Email or phone number")
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    full_name = forms.CharField(max_length  =256)
    username = forms.CharField(max_length=256)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        validators.validate_username_uniqueness(username)
        return username

    def clean_contact(self):
        contact = self.cleaned_data.get("contact")

        if validators.is_email(contact):
            self._handle_email(contact)
        elif validators.is_phone_number(contact):
            self._handle_phone(contact)
        else:
            raise ValidationError("Enter a valid email address or phone number.")

        return contact

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        validators.validate_passwords_match(password1, password2)
        return cleaned_data

    def save(self):
        return CustomUser.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password1"],
            full_name=self.cleaned_data["full_name"],
            email=self.cleaned_data.get("email"),
            phone_number=self.cleaned_data.get("phone_number"),

        )



    def _handle_email(self, email: str):
        validators.validate_email_format(email)
        validators.validate_email_uniqueness(email)
        self.cleaned_data["email"] = email

    def _handle_phone(self, phone: str):
        validators.validate_phone_uniqueness(phone)
        self.cleaned_data["phone_number"] = phone

class LoginForm(forms.Form):
    identifier = forms.CharField(max_length=150, label="Email,phone or username")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get("identifier")
        password = cleaned_data.get("password")
        user = authenticate(login=identifier,password=password)
        if user is None:
            raise ValidationError("Invalid login or password")

        self.user = user

        return cleaned_data

    def get_user(self):
        return self.user



