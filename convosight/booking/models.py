from django.db import models
from convosight.common.models import BaseModel
from convosight.booking.constants import BookingStatus


# Create your models here.
class Booking(BaseModel):
    """docstring for Booking"""

    user = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE
    )
    show = models.ForeignKey(
        'cinema.CinemaShow', on_delete=models.CASCADE
    )
    status = models.PositiveSmallIntegerField(
        choices=BookingStatus.CHOICES,
        default=BookingStatus.PROCESS
    )
    seat_selected = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.user.first_name)
