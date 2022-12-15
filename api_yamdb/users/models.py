from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER_ROLE_CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    ]
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=50,
        choices=USER_ROLE_CHOICES,
        default=USER
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=250,
        null=True,
        blank=False
    )
    bio = models.TextField(verbose_name='Биография', blank=True)
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user')
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        if self.is_staff:
            return self.role == self.ADMIN
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
