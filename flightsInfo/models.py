from django.db import models
from django import forms
from datetime import datetime


class Bus(models.Model):
    name = models.CharField(max_length=30)
    seats = models.SmallIntegerField()
    
    


class Appointments(models.Model):
    time = models.TimeField()

