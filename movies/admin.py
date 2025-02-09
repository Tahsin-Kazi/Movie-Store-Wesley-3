from django.contrib import admin
from django.utils.html import format_html
from .models import Review, Movie, Profile, Order

# admin.site.register(Review)
admin.site.register(Order)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_purchasedMovies', 'get_shoppingCart')
    search_fields = ('user',)  
    list_filter = ('user',) 
    ordering = ('user',)  

    def get_purchasedMovies(self, obj):
        return format_html("<br>".join([str(m) for m in obj.purchasedMovies.all()]))
    get_purchasedMovies.short_description = 'Purchased Movies' 

    def get_shoppingCart(self, obj):
        return format_html("<br>".join([str(m) for m in obj.shoppingCart.all()]))
    get_shoppingCart.short_description = 'Shopping Cart'  
    
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