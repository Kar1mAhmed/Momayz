# Generated by Django 4.2.6 on 2023-11-06 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0020_alter_program_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='auto_create',
            field=models.BooleanField(default=True),
        ),
    ]
