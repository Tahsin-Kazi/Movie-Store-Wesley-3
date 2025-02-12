# Generated by Django 5.1.5 on 2025-02-11 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_movie_age_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='purchasedMovies',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='shoppingCart',
        ),
        migrations.AddField(
            model_name='profile',
            name='purchasedMovies',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='profile',
            name='shoppingCart',
            field=models.JSONField(default=list),
        ),
    ]
