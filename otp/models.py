from django.db import models



class OTP(models.Model):
    phone = models.CharField(max_length=11)
    timestamp = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=6)