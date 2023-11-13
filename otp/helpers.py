from .models import OTP
from django.utils import timezone
from datetime import timedelta
import pytz

# Function to delete old OTPs
def delete_old_otps(passed_days=1):
    """
    Delete OTPs older than a specified number of days.

    Args:
        passed_days (int): Number of days for OTP expiration. Defaults to 1.
    """
    cairo_timezone = pytz.timezone('Africa/Cairo')
    current_date = timezone.now().astimezone(cairo_timezone).date()
    deletion_date = current_date - timedelta(days=passed_days)

    # Delete old OTPs
    OTP.objects.filter(created_at__lt=deletion_date).delete()