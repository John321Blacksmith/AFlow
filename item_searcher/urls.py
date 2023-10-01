from django.urls import path
from . import views

app_name = 'item_searcher'

urlpatterns = [
	path('', views.index, name='index'),
]