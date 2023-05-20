from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from api_yamdb.settings import LEN_TEXT


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

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
        blank=False,
        max_length=50,
        verbose_name='имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='фамилия'
    )
    role = models.CharField(
        max_length=15,
        choices=TYPE_MODELS,
        blank=True,
        verbose_name='роль'
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
        ordering = ('name',)
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
        ordering = ('name',)
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
        ordering = ('name', '-year',)
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

    class Meta:
        ordering = ('id',)


class Review(models.Model):
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение'
    )
    score = models.IntegerField(
        choices=RATING_CHOICES,
        default=None,
        verbose_name='оценка'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]
        ordering = ('-pub_date',)
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return self.text[:LEN_TEXT]


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        blank=False,
        related_name='comments',
        verbose_name='отзыв'
    )
    text = models.TextField(verbose_name='текст')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='дата публикации'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:LEN_TEXT]
