from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()
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


class Title(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    # author = models.ForeignKey(
    #    User, on_delete=models.CASCADE,
    #    null=True, blank=True, related_name='reviews')
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
    # author = models.ForeignKey(
    #     User, on_delete=models.CASCADE,
    #     null=True, blank=True, related_name='comments')
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
