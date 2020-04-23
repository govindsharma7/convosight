from django.db import models
from convosight.common.models import BaseModel


# Create your models here.
class Movie(BaseModel):
    """docstring for Movie"""

    name = models.CharField(max_length=150)
    release_date = models.DateTimeField()

    def __str__(self):
        return str(self.name)
