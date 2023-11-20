from django.db import models

from users.models import User

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    payment_id = models.IntegerField()
    created_at = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_method = models.CharField(max_length=50)
    pending = models.BooleanField()
    success = models.BooleanField()
    request = models.JSONField(null=True, blank=True)
