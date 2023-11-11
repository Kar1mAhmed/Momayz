# Generated by Django 4.2.6 on 2023-11-09 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0008_remove_subscription_passed_reservations_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='subscription', to='reservations.subscription'),
        ),
    ]