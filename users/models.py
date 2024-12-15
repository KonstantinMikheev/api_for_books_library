from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {'blank': True, 'null':True}

class User(AbstractUser):
    """Модель User для хранения информации о пользователях веб-приложения."""

    username = None
    email = models.EmailField(unique=True, verbose_name='email', help_text='Укажите почту')
    first_name = models.CharField(max_length=200, verbose_name='Имя', help_text='Укажите имя', **NULLABLE)
    last_name = models.CharField(max_length=200, verbose_name='Фамилия', help_text='Укажите фамилию', **NULLABLE)
    phone = PhoneNumberField(verbose_name="Номер телефона", help_text="Укажите номер телефона", **NULLABLE)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email} ({self.phone})'
