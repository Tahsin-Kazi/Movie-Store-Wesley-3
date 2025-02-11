# Generated by Django 5.1.5 on 2025-02-10 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='age_rating',
            field=models.CharField(choices=[('G', 'General Audience'), ('PG', 'Parental Guidance'), ('PG-13', 'Parents Strongly Cautioned'), ('R', 'Restricted'), ('NC-17', 'Adults Only'), ('NR', 'Not Rated')], default='PG', max_length=5),
        ),
    ]
