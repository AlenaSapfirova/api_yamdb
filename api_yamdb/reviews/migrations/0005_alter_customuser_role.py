# Generated by Django 3.2 on 2023-05-17 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_remove_customuser_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default='user', max_length=15),
        ),
    ]
