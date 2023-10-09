from django.db import models
from django import forms
from datetime import datetime


class Bus(models.Model):
    name = models.CharField(max_length=30)
    seats = models.SmallIntegerField()
    
    def __str__(self) -> str:
        return f"{self.name}({self.seats})"


class Appointments(models.Model):
    time = models.TimeField()
    
    class Meta:
        ordering = ['time']

    def __str__(self) -> str:
        return self.time
