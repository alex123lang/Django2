from django.contrib.auth.models import AbstractUser
from django.db import models
from catalog.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар', **NULLABLE)
    phone = models.CharField(max_length=20, verbose_name='Телефон', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='Страна', **NULLABLE)

    token = models.CharField(max_length=100, verbose_name='Token', **NULLABLE)

    def __str__(self):
        return self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
