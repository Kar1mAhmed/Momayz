# Generated by Django 4.2.6 on 2023-10-08 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
        ('flightsInfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlightDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.DurationField()),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='flightsInfo.bus')),
                ('move_at', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='flightsInfo.appointments')),
                ('move_from', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='move_from', to='locations.city')),
                ('move_to', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='move_to', to='locations.city')),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('available_seats', models.SmallIntegerField()),
                ('seats_count', models.SmallIntegerField()),
                ('cancelled', models.BooleanField(default=False)),
                ('details', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='flights.flightdetails')),
            ],
        ),
    ]
