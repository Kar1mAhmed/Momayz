# Generated by Django 4.2.6 on 2023-12-04 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0021_program_auto_create'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='canceled',
        ),
    ]
