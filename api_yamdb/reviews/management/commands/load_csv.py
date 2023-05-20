import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (
    Category,
    Comment,
    CustomUser,
    Genre,
    Review,
    Title,
    Title_Genre
)

FILES = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Title_Genre: 'genre_title.csv',
    CustomUser: 'users.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}

MODELS_FIELDS = {
    'author': ('author', CustomUser),
    'category': ('category', Category),
    'genre_id': ('genre', Genre),
    'review_id': ('review', Review),
    'title_id': ('title', Title)
}


def import_table(data):
    for key, value in data.items():
        if key in MODELS_FIELDS:
            if key[-3:] == '_id':
                data[key] = (
                    MODELS_FIELDS[key][1].objects.get(pk=value)
                ).id
            else:
                data[MODELS_FIELDS[key][0]] = (
                    MODELS_FIELDS[key][1].objects.get(pk=value)
                )
    return data


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, file_name in FILES.items():
            print(f'Импорт {file_name}')
            with open(
                f'{settings.BASE_DIR}/static/data/{file_name}',
                'r',
                encoding='utf-8'
            ) as data_file:

                csv_data = csv.DictReader(data_file)

                for data in csv_data:
                    import_table(data)
                    result = model(**data)
                    result.save()

        print(self.style.SUCCESS('Данные импортированы.'))
