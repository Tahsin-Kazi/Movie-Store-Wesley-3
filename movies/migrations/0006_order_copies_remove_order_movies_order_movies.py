# Generated by Django 5.1.5 on 2025-02-12 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_remove_order_movies_order_movies'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='copies',
            field=models.JSONField(default=list),
        ),
        migrations.RemoveField(
            model_name='order',
            name='movies',
        ),
        migrations.AddField(
            model_name='order',
            name='movies',
            field=models.ManyToManyField(related_name='orders', to='movies.movie'),
        ),
    ]
