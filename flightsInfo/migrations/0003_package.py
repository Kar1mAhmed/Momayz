# Generated by Django 4.2.6 on 2023-10-21 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flightsInfo', '0002_alter_appointments_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.SmallIntegerField()),
                ('num_of_flights', models.SmallIntegerField()),
                ('name', models.CharField(max_length=30)),
            ],
        ),
    ]
