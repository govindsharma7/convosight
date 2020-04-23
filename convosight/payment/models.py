from django.db import models
from convosight.common.models import BaseModel
from convosight.payment.constants import PaymentStatus


# Create your models here.
class Payment(BaseModel):
    """docstring for Payment"""

    booking = models.ForeignKey(
        'booking.Booking', on_delete=models.CASCADE
    )
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        choices=PaymentStatus.CHOICES,
        default=PaymentStatus.PROCESS
    )
    amount = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.name)
