# Generated by Django 5.1.5 on 2025-02-12 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_remove_profile_purchasedmovies_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='purchasedMovies',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='profile',
            name='shoppingCart',
            field=models.JSONField(default=dict),
        ),
    ]
