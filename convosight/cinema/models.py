from django.db import models
from django.db.models import Sum, Value as V
from django.db.models.functions import Coalesce
from convosight.common.models import BaseModel
from convosight.booking.models import Booking


# Create your models here.
class Cinema(BaseModel):
    """docstring for Cinema"""

    name = models.CharField(max_length=150)
    address = models.ForeignKey(
        'address.Address', on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.name)


class CinemaShow(BaseModel):
    """docstring for CinemaShow"""

    cinema = models.ForeignKey(
        'Cinema', on_delete=models.CASCADE
    )
    movie = models.ForeignKey(
        'movie.Movie', on_delete=models.CASCADE
    )
    show_date = models.DateField()
    show_start = models.TimeField()
    show_end = models.TimeField()
    seat_available = models.PositiveIntegerField(default=0)
    ticket_price = models.PositiveIntegerField()

    @property
    def available_seat_count(self):
        available = self.seat_available - get_available_seat_count(self.id)
        assert available >= 0
        return available

    def __str__(self):
        return str(self.cinema.name)


# Get company total unit
def get_available_seat_count(_id):
    total_count = Booking.objects.filter(
        show__id=_id,
    ).aggregate(total_count=Coalesce(Sum('seat_selected'), V(0)))

    return total_count.get('total_count')
