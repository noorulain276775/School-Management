from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MinLengthValidator
from phonenumber_field.modelfields import PhoneNumberField, validate_international_phonenumber
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, user_type='student', **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_parent(self, email, password=None, **extra_fields):
        return self.create_user(email, password, user_type='parent', **extra_fields)

    def create_student(self, email, password=None, **extra_fields):
        return self.create_user(email, password, user_type='student', **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('student', 'Student'),
    ]

    user_type = models.CharField(
        null=False, blank=False, max_length=20, choices=USER_TYPE_CHOICES)
    username = None
    first_name = models.TextField(
        null=False, blank=False, max_length=100, validators=[MinLengthValidator(2)])
    last_name = models.TextField(
        null=False, blank=False, max_length=100, validators=[MinLengthValidator(2)])
    phone = PhoneNumberField(null=False, blank=False, validators=[
                             validate_international_phonenumber])
    address = models.TextField(null=False, blank=False,
                               max_length=256, validators=[MinLengthValidator(9)])
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=False, blank=False,
                              max_length=100, unique=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Parent(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(
        upload_to='parent_images/', null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Subject(models.Model):
    subject_name = models.CharField(max_length=50)

    def __str__(self):
        return self.subject_name


class Teacher(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    subjects_taught = models.ManyToManyField(Subject, related_name='teachers')
    image = models.ImageField(
        upload_to='teacher_images/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Class(models.Model):
    class_name = models.CharField(max_length=10)
    grade_level = models.CharField(max_length=10)
    homeroom_teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, related_name='classes')

    def __str__(self):
        return self.class_name


class Student(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=10, unique=True)
    image = models.ImageField(
        upload_to='student_images/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    student_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.roll_number
