from django.contrib import admin
from .models import Review, Movie, Profile, Order

admin.site.register(Review)
admin.site.register(Movie)
admin.site.register(Order)

@admin.register(Profile)
class YourModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_purchasedMovies', 'get_shoppingCart')  # Display these fields in the list view
    search_fields = ('user',)  # Enable search by these fields
    list_filter = ('user',)  # Enable filtering by these fields
    ordering = ('user',)  # Ordering by field1

    def get_purchasedMovies(self, obj):
        return "\n".join([str(m) for m in obj.purchasedMovies.all()])
    def get_shoppingCart(self, obj):
        return "\n".join([str(m) for m in obj.shoppingCart.all()])