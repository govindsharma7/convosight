from django.urls import path
from convosight.cinema.views import (
    CinemaAPIView, CinemaShowAPIView, FilterCinemaShowList,
    CinemaList
)


app_name = 'cinema'

urlpatterns = [
    path('addCinema/', CinemaAPIView.as_view(), name="add_new_cinema"),
    path('addCinemaShow/', CinemaShowAPIView.as_view(), name="add_new_show"),
    path('allCinema/', CinemaList.as_view(), name="all_cinema_list"),
    path('filterShow/', FilterCinemaShowList.as_view(), name="filter_show"),
]
