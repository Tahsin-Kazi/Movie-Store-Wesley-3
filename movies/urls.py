from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>', views.show, name='movies.show'),
    
    # these 2 causing a lot of problems...
    path('edit_review/<int:id>/<int:review_id>', views.edit_review, name='movies.edit_review'),
    path('movies/create_review/<int:id>/', views.create_review, name='movies.create_review'),

]