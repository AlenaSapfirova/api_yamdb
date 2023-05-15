from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
# SUPERUSER = 'superuser'

TYPE_MODELS = [
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
    # (SUPERUSER,SUPERUSER)
]

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, 
                              blank=False,
                              max_length=250)
    username = models.CharField(max_length=100, unique=True, blank=False, validators=[RegexValidator(regex='^[\w.@+-]+\Z')])
    first_name = models.CharField(blank=False, max_length=20)
    last_name = models.CharField(max_length=50, blank=False)
    role = models.CharField(max_length=15, choices=TYPE_MODELS)
    bio = models.TextField()


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
        return self.role==USER
    
   
    def __str__(self):
        return f'{self.username} {self.email}'


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='категория'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='идентификатор категории'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='жанр'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='идентификатор жанра'
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='название'
    )
    year = models.IntegerField(
        verbose_name='год',
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='категория'
    )
    genre = models.ManyToManyField(
        Genre,
        through='Title_Genre',
        related_name='titles',
        verbose_name='жанр'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


class Title_Genre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )


