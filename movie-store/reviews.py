{% extends 'base.html' %}

# Reviews:
# 1. User name
# 2. Movie name
# 3. Star rating
# 4. Comments

# Add to admin page
# from .models import Movie, Review
#
# admin.site.register(Review)

from django.db import models
from django.contrib.auth. models import User

class Movie(models.Model):

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.Charfield(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str_(self):
        return str(self.id) + ' - ' + sels.movie.name