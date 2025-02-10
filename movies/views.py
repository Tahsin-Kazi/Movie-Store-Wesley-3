from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Order
from .forms import ReviewForm

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
    template_data = {"title": "Edit Review"} 
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
        return render(request, 'movies/edit_review.html', {'form': form, 'review': review, 'template_data': template_data})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=review.movie.id)

@login_required
def add_to_cart(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=movie_id)
        request.user.profile.shoppingCart.add(movie)
        request.user.profile.save()
        messages.success(request, f'{movie.name} has been added to your cart!')
        return redirect('movies.show', id=movie_id)
    return redirect('movies.show', id=movie_id)

@login_required
def remove_from_cart(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=movie_id)
        request.user.profile.shoppingCart.remove(movie) 
        request.user.profile.save()
        messages.success(request, f'{movie.name} has been removed from your cart!')
        return redirect('movies.view_cart')  
    return redirect('movies.view_cart') 

@login_required
def checkout(request):
    if request.method == 'POST':
        user = request.user.profile
        if not user.shoppingCart.all():
            messages.success(request, f'Order failed because cart is empty! Please add movies to checkout.')
            return redirect('movies.view_cart') 
        total = 0.0
        order = Order.objects.create(profile=user)
        order.count = user.shoppingCart.count()
        for movie in user.shoppingCart.all():
            total += movie.price
            user.purchasedMovies.add(movie)
            order.movies.add(movie)
        user.shoppingCart.clear()
        order.total = total
        order.save()
        user.save()
        messages.success(request, f'{order} has been fulfilled! Movies add to your library.')
        return redirect('home.index')
    messages.success(request, f'Error with order! Please try again later.')
    return redirect('movies.view_cart')  # Fallback redirect

@login_required
def view_cart(request):
    template_data = {"title": "Shopping Cart"}
    return render(request, 'movies/view_cart.html', {'cart_movies': request.user.profile.shoppingCart.all(), 'template_data': template_data})

@login_required
def delete_all_from_cart(request):
    if request.method == 'POST':
        cart = request.user.profile.shoppingCart.all()
        for movie in cart:
            request.user.profile.shoppingCart.remove(movie)
        messages.success(request, 'All items have been removed from your cart.')
    return redirect('movies.view_cart')