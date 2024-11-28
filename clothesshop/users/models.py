from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    image = models.ImageField(upload_to="users_images", blank=True, null=True, verbose_name='Image')
    phone = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='Phone number')
    birthday = models.DateField(blank=True, null=True, verbose_name='Birthday date')

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
