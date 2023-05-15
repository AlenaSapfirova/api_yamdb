import csv

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (
    Category,
    Genre,
    Title,
    Title_Genre,
    # Comment,
    # Review,
    # User
)

FILES = {

    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Title_Genre: 'genre_title.csv',

    # Comment: 'comments.csv',
    # Review: 'review.csv',
    # User: 'users.csv',
}

MODELS_FIELDS = {
    'category': ('category', Category),
    'title_id': ('title', Title),
    'genre_id': ('genre', Genre),
    # 'author': ('author', User),
    # 'review_id': ('review', Review),
}


def import_table(data):
    for key, value in data.items():
        if key in MODELS_FIELDS:
            data[MODELS_FIELDS[key][0]] = (
                MODELS_FIELDS[key][1].objects.get(pk=value)
            )
    return data


def import_manytomany(data):
    for key, value in data.items():
        if key in MODELS_FIELDS:
            data[key] = (
                MODELS_FIELDS[key][1].objects.get(pk=value)
            ).id
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
                    if file_name == 'genre_title.csv':
                        import_manytomany(data)
                    else:
                        import_table(data)

                    result = model(**data)
                    result.save()

        print(self.style.SUCCESS('Данные импортированы.'))
