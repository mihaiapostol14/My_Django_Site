from PIL import Image
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import FileExtensionValidator, validate_email
from django.db import models
from django.urls import reverse


# Create your models here.

class CustomUser(AbstractUser, PermissionsMixin):
    username = models.CharField(name='username', verbose_name='Username', unique=True,
                                validators=[UnicodeUsernameValidator],
                                max_length=50, null=True)
    email = models.EmailField(name='email', verbose_name='Email', max_length=254,
                              validators=[validate_email], null=True)
    password = models.CharField(name='password', verbose_name='Password', max_length=20, validators=[validate_password],
                                null=True)
    photo = models.ImageField(name='photo', verbose_name='Photo', default='default_account_picture.jpg',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg'],
                                                                 message='Your Photo Don’t have allowed extension')],
                              upload_to='user_photo',
                              null=True,
                              blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

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
