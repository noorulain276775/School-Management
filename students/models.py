from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField, validate_international_phonenumber
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    user_type = models.CharField(null=False, blank=False, max_length=20, choices=[(
        'parent', 'Parent'), ('teacher', 'Teacher'), ('admin', 'Admin'), ('student', 'Student')])
    first_name = models.TextField(
        null=False, blank=False, max_length=100, validators=[MinLengthValidator(2)])
    last_name = models.TextField(
        null=False, blank=False, max_length=100, validators=[MinLengthValidator(2)])
    phone = PhoneNumberField(null=False, blank=False, unique=True, validators=[
                             validate_international_phonenumber])
    address = models.TextField(null=False, blank=False,
                               max_length=256, validators=[MinLengthValidator(9)])
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=False, blank=False,
                              max_length=100, unique=True)
    objects = CustomUserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
