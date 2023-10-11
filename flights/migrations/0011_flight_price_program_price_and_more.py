# Generated by Django 4.2.6 on 2023-10-11 07:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0010_program_govern'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='price',
            field=models.SmallIntegerField(default=25, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='program',
            name='price',
            field=models.SmallIntegerField(default=25, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='flight',
            name='available_seats',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='flight',
            name='seats_count',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
