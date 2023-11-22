from .models import Payment
from rest_framework import serializers


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['transaction_id', 'amount_cents',  'success', 'created_at', 'created_at','payment_type']