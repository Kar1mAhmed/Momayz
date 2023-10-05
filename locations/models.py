from django.db import models
from django.db.models import ProtectedError


class Govern(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        # Check if there are related City instances.
        if self.city_set.exists():
            raise ProtectedError(
                "Cannot delete the Govern because it has related City instances.",
                self.city_set.all()
            )
        super().delete(*args, **kwargs)

class City(models.Model):
    name = models.CharField(max_length=30, unique=True)
    govern = models.ForeignKey(Govern, on_delete=models.CASCADE)

    def __str__(self):
        return self.name