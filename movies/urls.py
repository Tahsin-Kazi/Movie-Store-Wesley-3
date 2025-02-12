from django.urls import path
from . import views

urlpatterns = [
    path('movies/<int:id>/', views.show, name='movies.show'),
    path('reviews/edit/<int:review_id>/', views.edit_review, name='movies.edit_review'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='movies.delete_review'),
    path('add_to_cart/<int:movie_id>/', views.add_to_cart, name='movies.add_to_cart'),
    path('edit_cart/<int:movie_id>/', views.edit_cart, name='movies.edit_cart'),
    path('remove_from_cart/<int:movie_id>/', views.remove_from_cart, name='movies.remove_from_cart'),
    path('delete_all_from_cart/', views.delete_all_from_cart, name='movies.delete_all_from_cart'),
    path('cart/', views.view_cart, name='movies.view_cart'),
    path('checkout/', views.checkout, name='movies.checkout'),
]