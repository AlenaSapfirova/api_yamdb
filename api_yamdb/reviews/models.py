from django.db import models
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# User = get_user_model()

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
# SUPERUSER = 'superuser'

RATING_CHOICES = (
    (10, '10'),
    (9, '9'),
    (8, '8'),
    (7, '7'),
    (6, '6'),
    (5, '5'),
    (4, '4'),
    (3, '3'),
    (2, '2'),
    (1, '1'),
)

TYPE_MODELS = [
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
    # (SUPERUSER,SUPERUSER)
]


class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        blank=False,
        max_length=100
    )
    username = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z')]
    )
    first_name = models.CharField(blank=False, max_length=50)
    last_name = models.CharField(max_length=150, blank=False)
    role = models.CharField(max_length=15, choices=TYPE_MODELS, blank=True)
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
        return self.role == USER

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


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
       CustomUser,
       on_delete=models.CASCADE,
       null=True,
       blank=True,
       related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews', blank=True, null=True
    )
    score = models.IntegerField(
        choices=RATING_CHOICES,
        default=None,
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text[10]


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        null=True, blank=True, related_name='comments')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        blank=True, null=True
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text[10]
