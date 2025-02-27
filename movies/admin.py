from django.contrib import admin
from django.utils.html import format_html
from .models import Review, Movie, Profile, Order
from unfold.admin import ModelAdmin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('user', 'get_purchased_movies', 'get_shopping_cart')
    search_fields = ('user',)  
    list_filter = ('user',) 
    ordering = ('user',)
    
    def get_purchased_movies(self, obj):
        purchased_movies = obj.purchasedMovies
        if not purchased_movies:
            return "No purchased movies"
        return format_html("<br>".join([f"{Movie.objects.get(id=int(movie_id)).name} (x{count})" for movie_id, count in purchased_movies.items()]))
    get_purchased_movies.short_description = 'Purchased Movies'
    
    def get_shopping_cart(self, obj):
        shopping_cart = obj.shoppingCart
        if not shopping_cart:
            return "No items in cart"
        return format_html("<br>".join([f"{Movie.objects.get(id=int(movie_id)).name} (x{count})" for movie_id, count in shopping_cart.items()]))
    get_shopping_cart.short_description = 'Shopping Cart'
    
@admin.register(Movie)
class MovieAdmin(ModelAdmin):
    list_display = ('name', 'price', 'id', "age_rating")
    search_fields = ('name', 'price')
    list_filter = ('price', "age_rating")
    ordering = ('name',)
    
@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('movie', 'user', 'rating')
    search_fields = ('movie', 'user', 'rating')
    list_filter = ('rating', "movie")
    ordering = ('movie', 'user', 'rating')
    
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('profile', 'total', "get_movies", 'count')
    search_fields = ('profile', 'total', 'count', "get_movies")
    list_filter = ('created_at',)
    ordering = ("-created_at",)
    
    def get_movies(self, obj):
        movies = [
            f"{movie.name} (x{count})"
            for movie, count in zip(obj.movies.all(), obj.copies)
        ]
        return format_html("<br>".join(movies))
    get_movies.short_description = 'Purchased Movies'