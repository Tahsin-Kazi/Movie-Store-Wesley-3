from django.contrib import admin
from .models import Review, Movie, Profile

admin.site.register(Review)
admin.site.register(Movie)
admin.site.register(Profile)