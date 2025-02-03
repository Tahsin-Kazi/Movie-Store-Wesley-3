from django.shortcuts import render, redirect, reverse
from .models import Movie, Review
from .forms import ReviewForm

movies = [
    {
        'id': 1, 'name': 'Inception', 'price': 12,
        'description': 'A mind-bending heist thriller.'
    },
    {
        'id': 2, 'name': 'Avatar', 'price': 13,
        'description': 'A journey to a distant world and the battle for resources.'
    },
    {
        'id': 3, 'name': 'The Dark Knight', 'price': 14,
        'description': 'Gothams vigilante faces the Joker.'
    },
    {
        'id': 4, 'name': 'Titanic', 'price': 11,
        'description': 'A love story set against the backdrop of the sinking Titanic.',
    },
]
def index(request):
    # movie = movies[id - 1]
    template_data = {}
    template_data['title'] = "Movies"
    # template_data['movies'] = movies
    return render(request, 'movies/show.html',
                  {'template_data': template_data})

def show(request, id):
    movie = movies[id - 1]
    template_data = {}
    template_data['title'] = movie['name']
    template_data['movie'] = movie
    create_review_url = reverse('movies.create_review', kwargs={'id': template_data['movie']['id']})
    template_data['create_review_url'] = create_review_url
    return render(request, 'movies/show.html', {'template_data': template_data})
    
    
    
# create and edit not functional yet

def edit_review(request, id, review_id):
    movie = Movie.objects.get(id=id)
    review = Review.objects.get(id=review_id)
    
    if request.method == 'POST':
        review.comment = request.POST.get('comment')
        review.save()
        return redirect('movies.show', id=movie.id)
    
    template_data = {}
    template_data['movie'] = movie
    template_data['review'] = review
    
    return render(request, 'movies/edit_review.html', {'template_data': template_data})

def create_review(request, id):
    movie = Movie.objects.get(id=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.save()
            return redirect('movies.show', id=movie.id)
    else:
        form = ReviewForm()
    return render(request, 'movies/create_review.html', {'form': form, 'movie': movie})