# Generated by Django 4.2.6 on 2023-10-19 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_alter_reservation_reserved_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reservation',
            options={'ordering': ['flight__date', 'flight__time']},
        ),
    ]
