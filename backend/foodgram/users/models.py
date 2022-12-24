from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q
from foodgram.settings import EMAIL_MAX_LENGTH, NAME_MAX_LENGTH

from .validators import check_username

FOLLOW_STR = '{user} подписан на {author}'


class User(AbstractUser):
    """Модель пользователя."""
    ADMIN = 'admin'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Админ'),
        (USER, 'Пользователь'),
    ]

    username = models.CharField(
        validators=[check_username],
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

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return (
            self.role == self.ADMIN
            or self.is_staff
        )


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower', verbose_name='Подписчик')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='уникальная подписка'
            ),
            models.CheckConstraint(
                check=Q(user=F('user')),
                name='подписка на самого себя'
            )
        ]

    def __str__(self):
        return FOLLOW_STR.format(
            user=self.user.username,
            author=self.author.username
        )
