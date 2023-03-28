from django.urls import path
from app_movie import views

app_name="app_movie"

urlpatterns=[
    path('', views.moviesInfo, name="moviesInfo"),
    path('results/', views.results, name="results"),
    path('api_get_movies', views.api_get_movies, name='api_get_movies'),
    path('api_get_pages', views.api_get_pages, name='api_get_pages'),
    path('api_get_movie_by_title', views.api_get_movie_by_title, name='api_get_movie_by_title'),
    path('api_search_by_title', views.api_search_by_title, name='api_search_by_title'),
]