from django.shortcuts import render

from app.models import Movie

def index(request):
	print(Movie.objects.count())
	return render(request, 'index.html', {'year': '2001', 'rating': '8.3', 'hours': '2', 'minutes': '32', 'genres': 'Adventure, Family, Fantasy'})
