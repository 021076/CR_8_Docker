from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    tg_chat_id = models.CharField(max_length=50, verbose_name='telegram chat_id', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
