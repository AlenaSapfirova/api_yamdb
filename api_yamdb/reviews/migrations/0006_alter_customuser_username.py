# Generated by Django 3.2 on 2023-05-13 13:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20230513_0249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator(regex='^[\\w.@+-]+\\Z')]),
        ),
    ]