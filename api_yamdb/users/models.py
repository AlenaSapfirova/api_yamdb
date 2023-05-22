from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


TYPE_MODELS = [
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
]

class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        blank=False,
        max_length=100,
        verbose_name='адрес почты'
    )
    username = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z')],
        verbose_name='ник'
    )
    first_name = models.CharField(
        blank=True,
        max_length=50,
        verbose_name='имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='фамилия'
    )
    role = models.CharField(
        max_length=15,
        choices=TYPE_MODELS,
        blank=True,
        verbose_name='роль',
        default='user'
    )
    bio = models.TextField(verbose_name='биография')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('id',)

    def __str__(self):
        return f'{self.username} {self.email}'
