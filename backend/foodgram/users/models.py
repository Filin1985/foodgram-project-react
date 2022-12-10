from django.db import models
from django.contrib.auth.models import AbstractUser

from foodgram.settings import NAME_MAX_LENGTH, EMAIL_MAX_LENGTH

class User(AbstractUser):
    """Модель пользователя."""
    ADMIN = 'admin'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Админ'),
        (USER, 'Пользователь'),
    ]

    username = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Имя пользователя'
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        verbose_name='Электронная почта'
    )
    first_name = models.CharField(max_length=NAME_MAX_LENGTH, blank=True)
    last_name = models.CharField(max_length=NAME_MAX_LENGTH, blank=True)
    role = models.CharField(
        max_length=max(len(value) for value, _ in ROLES),
        choices=ROLES,
        default=USER,
        verbose_name='Роль'
    )

    @property
    def is_admin(self):
        return (
            self.role == self.ADMIN
            or self.is_staff
        )

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
