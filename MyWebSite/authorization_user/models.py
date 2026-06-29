from PIL import Image
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.core.validators import FileExtensionValidator, validate_email
from django.db import models
from django.urls import reverse

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)



# Create your models here.

class User(AbstractUser, PermissionsMixin):
    username = None
    first_name = models.CharField(name='first_name', verbose_name='First Name', max_length=50,
                                null=True)
    last_name = models.CharField(name='last_name', verbose_name='Last Name', max_length=50,
                                null=True)
    email = models.EmailField(name='email', verbose_name='Email', max_length=254,
                              validators=[validate_email], unique=True)
    password = models.CharField(name='password', verbose_name='Password', max_length=20, validators=[validate_password],
                                null=True)
    photo = models.ImageField(name='photo', verbose_name='Photo', default='default_account_picture.jpg',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg'],
                                                                 message='Your Photo Don’t have allowed extension')],
                              upload_to='user_photo',
                              null=True,
                              blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_photo(self):
        return self.photo.url

    def get_absolute_url(self):
        return reverse(viewname='authorization_user', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)
