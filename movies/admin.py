from django.contrib import admin
from django.utils.html import format_html
from .models import Review, Movie, Profile, Order

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user',)  
    list_filter = ('user',) 
    ordering = ('user',)
    
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'id')
    search_fields = ('name', 'price')
    list_filter = ('price',)
    ordering = ('name',)
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating')
    search_fields = ('movie', 'user', 'rating')
    list_filter = ('rating',)
    ordering = ('movie', 'user', 'rating')
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('profile', 'total', "get_movies", 'count')
    search_fields = ('profile', 'total', 'count', "get_movies")
    list_filter = ('total', 'count', 'created_at')
    ordering = ('profile', 'total', 'count',)
    
    def get_movies(self, obj):
        return format_html("<br>".join([str(m) for m in obj.movies.all()]))

    def get_review(self, obj):
        return "\n".join([str(m) for m in obj.review.all()])