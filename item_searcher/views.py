from django.shortcuts import render
from .import models

# Create your views here.


def index(request):
	context = {'content': None}
	return render(request, 'item_searcher/index.html', context=context)