from django.db import models
from convosight.common.models import BaseModel


# Create your models here.
class Address(BaseModel):
    """docstring for Address"""

    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, null=True, blank=True)
    latitude = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        address = self.address1
        if self.address2:
            address = ", " + self.address2
        return address + " -->> " + str(self.id)

    def get_full_address(self):
        """ Returns Full Address """

        full_address = ""

        address1 = (self.address1 or '').strip()
        if len(address1) > 0:
            full_address = address1
        address2 = (self.address2 or '').strip()
        if len(address2) > 0:
            full_address = full_address + address2
        zipcode = (self.zipcode)
        if len(zipcode) > 0:
            full_address = '\n'.join([full_address, zipcode])
        city = (self.city)
        if len(city) > 0:
            full_address = '\n'.join([full_address, city])
        state = (self.state)
        if len(state) > 0:
            full_address = '\n'.join([full_address, state])
        country = (self.country)
        if len(country) > 0:
            full_address = '\n'.join([full_address, country])
        return full_address
