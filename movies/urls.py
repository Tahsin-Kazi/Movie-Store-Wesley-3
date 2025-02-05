from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.index, name='movies.index'),
    path('movies/<int:id>/', views.show, name='movies.show'),
    path('reviews/edit/<int:review_id>/', views.edit_review, name='movies.edit_review'),
]