from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from .forms import ReviewForm

#imports for search bar
from tkinter import *
import webbrowser
from tkinter import Entry


def index(request):
    template_data = {'title': "Movies", 'movies': Movie.objects.all()}
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

#Search Bar stuff
def search(request):

    root = Tk()

    root.title("search tab")

    def search():
        url = entry.get()
        webbrowser.open(url)

    label1 = Label(root, text="Enter Movie Title", font=("Arial", 20))
    label1.grid(row=0, column=0)

    entry = Entry(root, width=30)
    entry.grid(row=0, column=1)

    button = Button(root, text="Search", command=search)

    button.grid(row=1, column=0, columnspan=2, pady=10)

    root.mainloop()