from django.urls import path
from convosight.movie.views import (
    MovieAPIView, MoviesList
)


app_name = 'movie'

urlpatterns = [
    path('addMovie/', MovieAPIView.as_view(), name="add_new_movie"),
    path('allMovie/', MoviesList.as_view(), name="movies_list"),
]
