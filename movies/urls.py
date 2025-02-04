from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>', views.show, name='movies.show'),

    #path for the reviews
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
]