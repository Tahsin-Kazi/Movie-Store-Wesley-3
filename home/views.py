from django.shortcuts import render
from movies.models import Movie

def index(request):

    #Search bar
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'GT Movies Store'
    template_data['movies'] = movies
    return render(request, 'home/index.html',
                  {'template_data': template_data})

def about(request):
    template_data = {'title': 'About'}
    return render(request, 'home/about.html', {"template_data": template_data})