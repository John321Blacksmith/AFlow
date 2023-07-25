from django.shortcuts import render

# Create your views here.


def search(request):
	return render(request, 'templates/search.html')


def get_results(request):
	return render(request, 'templates/results.html')