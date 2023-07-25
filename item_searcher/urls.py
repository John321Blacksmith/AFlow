from django.urls import path
from . import views

app_name = 'item_searcher'
urlpatterns = [
	path('', views.search, name='search'),
	path('results/', views.get_results, name='results'),
]

