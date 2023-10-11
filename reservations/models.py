from django.db import models
from users.models import User
from flights.models import Flight


class reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.PROTECT)
    reserved_at = models.DateTimeField(auto_created=True)
    seat_number = models.SmallIntegerField()
