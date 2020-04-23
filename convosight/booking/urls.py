from django.urls import path
from convosight.booking.views import (
    BookingAPIView, BookingListAPIView
)


app_name = 'booking'

urlpatterns = [
    path('bookTicket/', BookingAPIView.as_view(), name="book_show"),
    path('allBooking/', BookingListAPIView.as_view(), name="booking_list"),
]
