from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>', views.show, name='movies.show'),

    #path for the reviews
    path('reviews/edit/<int:review_id>/', views.edit_review, name='movies.edit_review'),

]