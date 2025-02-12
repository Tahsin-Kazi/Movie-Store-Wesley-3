from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Order
from .forms import ReviewForm, BuyForm, EditCartForm


def show(request, id):
    movie = get_object_or_404(Movie, id=id)
    template_data = {
        'title': movie.name,
        'movie': movie,
        'reviews': get_reviews(id),
        'avg_review': avg_review(id),
        'age_rating': movie.age_rating
    }
    r_form = ReviewForm()
    b_form = BuyForm()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movies.show', id=movie.id)
        
    return render(request, 'movies/show.html', {'template_data': template_data, 'r_form': r_form, 'b_form': b_form})

def get_reviews(id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie).order_by('-created_at')
    return reviews

def avg_review(id):
    reviews = get_reviews(id)
    if not reviews:
        return str("Unrated")
    else:
        total = 0
        for review in reviews:
            total += review.rating
            total = round(total, 1)
        return total / len(reviews)

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
        form = BuyForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            movie = get_object_or_404(Movie, id=movie_id)
            cart = request.user.profile.shoppingCart
            if str(movie_id) in cart:
                cart[str(movie_id)] += quantity
            else:
                cart[str(movie_id)] = quantity
            request.user.profile.save()
            messages.success(request, f'{quantity} copies of {movie.name} have been added to your cart!')
            return redirect('movies.show', id=movie_id)
    return redirect('movies.show', id=movie_id)

@login_required
def remove_from_cart(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=movie_id)
        request.user.profile.shoppingCart.pop(str(movie_id))
        request.user.profile.save()
        messages.success(request, f'{movie.name} has been removed from your cart!')
        return redirect('movies.view_cart')  
    return redirect('movies.view_cart')

@login_required
def edit_cart(request, movie_id):
    if request.method == 'POST':
        quantity = request.POST.get('edit_quantity')
        movie = get_object_or_404(Movie, id=movie_id)
        request.user.profile.shoppingCart[(str(movie_id))] = quantity
        request.user.profile.save()
        messages.success(request, f'{movie.name} has been edited in your cart!')
        return redirect('movies.view_cart')
    return redirect('movies.view_cart')

@login_required
def checkout(request):
    if request.method == 'POST':
        user = request.user.profile
        if not user.shoppingCart:
            messages.error(request, 'Order failed because cart is empty! Please add movies to checkout.')
            return redirect('movies.view_cart') 
        total = 0.0
        total_count = 0
        order = Order.objects.create(profile=user)
        for movie_id, quantity in user.shoppingCart.items():
            movie = Movie.objects.get(id=movie_id)
            quantity = int(quantity)
            total += float(movie.price * quantity)
            total_count += quantity
            if str(movie_id) in user.purchasedMovies:
                user.purchasedMovies[str(movie_id)] += quantity
            else:
                user.purchasedMovies[str(movie_id)] = quantity
            order.movies.add(movie)
            order.copies.append(quantity)
        user.shoppingCart.clear()
        order.total = total
        order.count = total_count
        order.save()
        user.save()
        messages.success(request, 'Your order has been fulfilled! Movies added to your library.')
        return redirect('home.index')
    messages.error(request, 'Error with order! Please try again later.')
    return redirect('movies.view_cart')

@login_required
def view_cart(request):
    template_data = {"title": "Shopping Cart"}
    cart = request.user.profile.shoppingCart
    movies = []
    order_total = 0.0
    for movie_id, quantity in cart.items():
        movie = get_object_or_404(Movie, id=movie_id)
        total_cost = movie.price * quantity
        order_total += total_cost
        movies.append((movie, quantity, total_cost))
    return render(request, 'movies/view_cart.html', {'cart_movies': movies, 'order_total': order_total, 'template_data': template_data, 'e_form': EditCartForm()})

@login_required
def delete_all_from_cart(request):
    if request.method == 'POST':
        request.user.profile.shoppingCart.clear()
        request.user.profile.save()
        messages.success(request, 'All items have been removed from your cart.')
    return redirect('movies.view_cart')