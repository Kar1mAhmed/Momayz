from django.db import models



class Package(models.Model):
    price = models.SmallIntegerField()
    num_of_flights = models.SmallIntegerField()
    name = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return self.name



class Bus(models.Model):
    name = models.CharField(max_length=30)
    seats = models.SmallIntegerField()
    
    def __str__(self) -> str:
        return f"{self.name}({self.seats})"




class Appointments(models.Model):
    time = models.TimeField()
    
    class Meta:
        ordering = ['time']

    def __str__(self):
        return self.time.strftime('%I:%M %p')  # This formats the time as 12-hour with AM/PM