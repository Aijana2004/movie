# Generated by Django 5.1 on 2024-08-27 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_favorites'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Favorites',
            new_name='Favorite',
        ),
    ]
