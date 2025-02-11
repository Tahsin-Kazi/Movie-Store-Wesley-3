from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Movie(models.Model):
    AGE_RATINGS = [
        ('G', 'General Audience'),
        ('PG', 'Parental Guidance'),
        ('PG-13', 'Parents Strongly Cautioned'),
        ('R', 'Restricted'),
        ('NC-17', 'Adults Only'),
        ('NR', 'Not Rated'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    age_rating = models.CharField(max_length=5, choices=AGE_RATINGS, default='PG')
    price = models.IntegerField()
    description = models.TextField()
    image = models.FileField(upload_to='movies/')
    def __str__(self):
        return self.name

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Movie: {self.movie.name}; User: {self.user.username}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    purchasedMovies = models.ManyToManyField(Movie, related_name='purchased_movies')
    shoppingCart = models.ManyToManyField(Movie, related_name='shopping_cart')

    def __str__(self):
        return f"{self.user.username}"

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        try:
            instance.profile.save()
        except:
            Profile.objects.create(user=instance)

class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie, related_name='orderedMovies')
    total = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile}'s order of {self.count} movies for {self.total} at {self.created_at}"