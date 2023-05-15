from django.db import models


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
