from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from .forms import ReviewForm


def index(request):

    #Search bar
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    #Template Data
    #template_data = {'title': "Movies", 'movies': Movie.objects.all()}
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})

def show(request, id):
    movie = get_object_or_404(Movie, id=id)
    template_data = {
        'title': movie.name,
        'movie': movie,
        'reviews': get_reviews(id)
    }
    form = ReviewForm()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movies.show', id=movie.id)
        
    return render(request, 'movies/show.html', {'template_data': template_data, 'form': form})

def get_reviews(id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie).order_by('-created_at')
    return reviews

@login_required
def edit_review(request, review_id):
    review = Review.objects.get(id=review_id)

    if request.user != review.user:
        return redirect('movies.show', movie_id=review.movie.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updatedReview = form.save(commit=False)
            updatedReview.save()
            return redirect('movies.show', id=review.movie.id)  # Use redirect instead of show
    else:
        form = ReviewForm(instance=review)
        return render(request, 'movies/edit_review.html', {'form': form, 'review': review})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=review.movie.id)

