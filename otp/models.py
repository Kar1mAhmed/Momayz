from django.db import models


class OTP(models.Model):
    phone_number = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=6)
